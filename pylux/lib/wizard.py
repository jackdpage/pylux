# Your friendly neighbourhood wizard

NAME = 'Merlyn'
DISPLAY_NAME = '[Merlyn] '

def say(s):
    '''Make the wizard say something in a wizard voice.'''
    print(DISPLAY_NAME+s)

def ask(q, default=False):
    '''Make the wizard ask a question.'''
    if not default:
        ans = input(DISPLAY_NAME+q+': ')
    else:
        ans = input(DISPLAY_NAME+q+' ['+str(default)+']: ')
        if ans == '':
            return default
    return ans
