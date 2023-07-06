from typing import List
from dataclasses import dataclass
import datetime
import os
import xml.etree.ElementTree as ET


@dataclass
class Question:
    text: str
    answers: List[str]
    correct_answer: int

    @property
    def enum_answers(self):
        return enumerate(self.answers)


@dataclass
class Quiz:
    title: str
    questions: List[Question]
    last_modified: datetime.datetime
    path: str

    @property
    def enum_questions(self):
        return enumerate(self.questions)

    def needs_update(self):
        return self.last_modified < datetime.datetime.fromtimestamp(
            os.path.getmtime(self.path))


def parse_quiz(file_name: str) -> Quiz:
    last_modified = datetime.datetime.fromtimestamp(
        os.path.getmtime(file_name))
    tree = ET.parse(file_name)
    root = tree.getroot()

    assert root.tag == "quiz"

    title = root.attrib.get("title", "Quiz")

    questions = []
    for question in root.findall("question"):
        question_text = question.find("text").text
        answers = []
        correct_answer = None
        for i, answer in enumerate(question.findall("answer")):
            assert answer.tag == "answer"
            answer_text = answer.text
            if answer.attrib.get("correct", "false") == "true":
                correct_answer = i
            answers.append(answer_text)
        assert correct_answer is not None
        answers = [answer.text for answer in question.findall("answer")]
        questions.append(Question(question_text, answers, correct_answer))

    return Quiz(title, questions, last_modified, file_name)
