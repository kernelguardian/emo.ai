import jinja2
import os
import webbrowser


templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)

recommendations = "1.JOURNAL IT ALL OUT \
    Keep a notebook or journal where you can record your situations, how to respond to it,\
    how can you improve and organise your thoughts etc \
    And slowly you could get a grip of yourself and a relief from your stress at the end."


def gen(emo, dict_value):
    if len(emo) > 1:
        if emo[0] == 'neutral':
            dominant_emotion = emo[1]
        else:
            dominant_emotion = emo[0]
    else:
        dominant_emotion = emo[0]

    if dominant_emotion == 'happy':
        message_for_insertion = "Wouldn't it be great if you could cheer up others too?"
    else:
        message_for_insertion = "We understand that it can be difficult to accept certain things in life. \
            So to help you have a better life we have added certain tasks for you to take upon \
                that would refresh your mind."

    outputText = template.render(
        username=dict_value['q1'], emotion=dominant_emotion, message=message_for_insertion, q2=dict_value['q2'], q3=dict_value['q3'],
        q4=dict_value['q4'], q5=dict_value['q5'], q6=dict_value['q6'], q7=dict_value['q7'], q8=dict_value['q8'], q9=dict_value['q9'], q10=dict_value['q10'], q11=dict_value['q11'], q12=dict_value['q12'])

    html_file = open('processed' + '.html', 'w')
    html_file.write(outputText)
    html_file.close()
    webbrowser.open_new("processed.html")
    # os.system(
    #     'cmd /c "pandoc processed.html -V geometry:margin=0.5in -o Report.pdf"')
    # os.remove("processed.html")
    # pdfkit.from_file('processed.html', 'Report.pdf')


# dict_va = dict({'q1': 'a', 'q2': 'a', 'q3': 'a', 'q4': 'a',
#                 'q5': 'a', 'q6': 'a', 'q7': 'a', 'q8': 'a', 'q9': 'a', 'q10': 'a', 'q11': 'a', 'q12': 'a'})
# gen('happy', dict_va)
