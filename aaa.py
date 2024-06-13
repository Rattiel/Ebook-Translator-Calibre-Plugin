import re

# punctuation_pattern = r'(["\'「」『』.。!?~])\s*'


test_pattern = r'(["\'「」『』.。!?~\()])\s*'

"""
punctuation_marks = ['"', "'", '「', '」', '『', '』', '\[', '\]', '\{', '\}', '\(', '\)']
punctuation_spliter = "".join(punctuation_marks)
punctuation_pattern = r'([' + punctuation_spliter + r'])\s*'
"""

"""
white_space_marks = [' ']
divide_marks = ['"', "'", '「', '」', '『', '』', '\[', '\]', '\{', '\}', '(', ')']
punctuation_marks = ['…', '\n', '.', '。', '!', '?', '~']
punctuation_spliter = "".join(divide_marks)
punctuation_spliter = punctuation_spliter.join(punctuation_marks)
punctuation_pattern = r'([' + punctuation_spliter + r'])\s*'
translate_ignore_mark = divide_marks + punctuation_marks + white_space_marks + ['', '[', ']', '(', ')', '{', '}']
white_space_add_marks = punctuation_marks + white_space_marks
"""

zero_space = ''
white_space = ' '
japanese_mark = {
    '。': '.',
    '（': "(",
    '）': ")",
    '！': '!',
    '？': '?'
}

divide_patterns = ['"', "'", '「', '」', '『', '』', '\[', '\]', '\{', '\}', '(', '（', ')', '）']
divide_marks = ['"', "'", '「', '」', '『', '』', '[', ']', '{', '}', '(', '（', ')', '）']

punctuation_patterns = ['…', '\n', '.', '。', '!', '！', '?', '？', '~', '～', '\-', '─']
punctuation_marks = ['…', '\n', '.', '。', '!', '！', '?', '？', '~', '～', '-', '─']

punctuation_pattern = r'([' + "".join(divide_patterns + punctuation_patterns) + r'])\s*'
translate_ignore_mark = divide_marks + punctuation_marks + [white_space, zero_space]
white_space_not_need_marks = [white_space, zero_space] + punctuation_marks + divide_marks

# text = "('hello' world. ! asdsa)[a]{b}"
text = "月明かりが差し込む室内、ユミはグランドピアノの前に腰掛けている。が、ただそれだけだった。鍵盤の蓋を開けるでもなく、その視線は鍵盤と譜面台の間辺りにじっと注がれている……ように見えて、その実何も見てはいなかった。"

split_text = re.split(punctuation_pattern, text)

result = ""
split_text_len = len(split_text)
for index, target_text in enumerate(split_text):

    if target_text not in translate_ignore_mark:
        print(str(index) + ": " + target_text + " -t")

        if index > 1 and split_text[index - 1] in punctuation_marks:
            result += white_space
        result += ("{{" + target_text + "}}")
    else:
        print(str(index) + ": " + target_text)
        if target_text in japanese_mark:
            result += japanese_mark[target_text]
        else:
            result += target_text

print(text)
print(result)
