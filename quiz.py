from typing import List, NoReturn, Optional, Tuple, Union


class Quiz:
    """
    A quiz.

    Style for a question:
    - Each question should be a `tuple` of 3 items:
        * `int`: the type of the question
            + `0` = choice
            + `1` = free
        * `str`: the question text
        * `List[str] | None`: options for question whose `type=0`, `None` 
            elsewise
    """
    def __init__(self):
        self.questions: List[Tuple[int, str, Optional[List[str]]]] = []

    def add_question(self, type: int, text: str, options: Optional[List[str]] = None) -> Tuple[int, str, Optional[List[str]]]:
        q = (type, text, options)
        self.questions.append(q)
        return q

    def add_questions(self, *args: Union[int, str, List[str], None]) -> NoReturn:
        for q in zip(args[::3], args[1::3], args[2::3]):
            self.add_question(*q)

    def remove_question(self, index: int) -> Tuple[int, str, Optional[List[str]]]:
        return self.questions.pop(index)

    def get_question(self, index: int) -> Tuple[int, str, Optional[List[str]]]:
        return self.questions[index]

    def get_questions_html(self, *indices: int) -> str:
        i = 1
        main_html = '''\
<div class="question">%s

</div>'''
        for index in indices:
            q = self.questions[index]
            if q[0] == 0:
                html = '''\


    <div class="question-choice"><strong>%i</strong>. %s</div>
    <div class="question-choice-choices">
''' % (i, q[1])
                for ci in range(len(q[2])):
                    c = q[2][ci]
                    html += '''\
        <input type="radio" name="question-choice-%i" id="question-choice-%i-%i" value="%i">
        <label for="question-choice-%i-%i">%s</label>
''' % (i, i, ci, ci, i, ci, c)
                html += '    </div>%s'
            elif q[0] == 1:
                html = '''\


    <div class="question-free"><strong>%i</strong>. %s</div>
    <div class="question-free-input">
        <textarea name="question-free-%i" id="question-free-%i"></textarea>
    </div>%%s''' % (i, q[1], i, i)
            else:
                html = '''\


    <div class="question-unknown>
        <strong>UNKNOWN QUESTION FORMAT</strong>
    </div>%s'''
            main_html %= html
            i += 1
        main_html %= ''
        return main_html


if __name__ == '__main__':
    q = Quiz()
    q.add_questions(0, 'How are you?', ['Good!', 'Happy!', 'Nice!'], 1, 'How\'s the weather today?', None)
    print(q.get_questions_html(0, 1))
