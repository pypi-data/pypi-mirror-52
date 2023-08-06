import logging
import json
import zmq
import os

from util import *

logger = logging.getLogger(__name__)


class TabooJudger:
    def __init__(self, task_setting, attack_host="127.0.0.1", attack_port=10086, defend_host="127.0.0.1",
                 defend_port=10087):
        self.task_setting = task_setting
        self.history = {
            "task_setting": task_setting
        }

        self.attacker_context = zmq.Context()
        self.attacker = self.attacker_context.socket(zmq.REQ)
        self.attacker.connect("tcp://%s:%d" % (attack_host, attack_port))

        self.attacker.send_json({
            "code": INIT,
            "data": self.task_setting
        })
        data = self.attacker.recv_json()
        if data["code"] != ATTACKER_FEEDBACK:
            logger.error("Unknown code, bad attacker.")
            raise NotImplementedError
        else:
            self.attacker_name = data["data"]

        logger.info("Connected to attacker %s:%d" % (attack_host, attack_port))

        self.defender_context = zmq.Context()
        self.defender = self.defender_context.socket(zmq.REQ)
        self.defender.connect("tcp://%s:%d" % (defend_host, defend_port))

        self.defender.send_json({
            "code": INIT,
            "data": self.task_setting
        })
        data = self.defender.recv_json()
        if data["code"] != DEFENDER_FEEDBACK:
            logger.error("Unknown code, bad defender.")
            raise NotImplementedError
        else:
            self.defender_name = data["data"]

        logger.info("Connected to defender %s:%d" % (defend_host, defend_port))

    def select_word(self, word_list):
        self.history["word_list"] = word_list
        logger.info("Word candidate set: %s" % json.dumps(word_list, ensure_ascii=False))
        self.attacker.send_json({
            "code": WORD_SELECT,
            "data": word_list
        })
        data = self.attacker.recv_json()
        if data["code"] != WORD_SELECT:
            logger.error("Unknown code, bad attacker.")
            raise NotImplementedError

        self.word = word_list[data["data"]]
        self.history["select_word"] = self.word
        logger.info("Attacker selects the word: %s" % self.word)

        self.attacker.send_json({
            "code": RECEIVED,
            "data": RECEIVED
        })

    def play_game(self, checker, formatter, ruler):
        self.history["sentences"] = []

        while True:
            attack_msg = self.attacker.recv_json()
            if attack_msg["code"] != ATTACK:
                logger.error("Unknown code, bad attacker.")
                raise NotImplementedError

            attack_msg = formatter.format(attack_msg["data"])
            self.history["sentences"].append(attack_msg)
            logger.info("Attacker says: %s" % attack_msg)

            self.defender.send_json({
                "code": DEFEND,
                "data": attack_msg
            })

            defend_msg = self.defender.recv_json()
            if defend_msg["code"] == ACTIVELY_GUESS:
                pass
            elif defend_msg["code"] == DEFEND:
                defend_msg = formatter.format(defend_msg["data"])
                self.history["sentences"].append(defend_msg)
                logger.info("Defender says: %s" % defend_msg)
                if checker.check(defend_msg, self.word):
                    self.attacker.send_json({
                        "code": ATTACKER_WIN,
                        "data": defend_msg
                    })
                    self.defender.send_json({
                        "code": ATTACKER_WIN,
                        "data": self.word
                    })
                    self.history["result"] = "Attacker wins."
                    logger.info("Attacker wins")
                    break
                else:
                    self.attacker.send_json({
                        "code": ATTACK,
                        "data": defend_msg
                    })
            else:
                logger.error("Unknown code, bad defender.")
                raise NotImplementedError


if __name__ == "__main__":
    os.system("clear")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)

    judger = TabooJudger({}, attack_port=23333)
    judger.select_word(["apple", "peach", "ubuntu", "windows", "hello", "what", "fuck"])

    from taboo import formatter, ruler, checker

    judger.play_game(checker.TabooEnglishChecker(), formatter.TabooStupidFormatter(), ruler.TabooStupidRuler())
