import subprocess
import openai
import os


OPENAI_API_KEY = ""
LATEX_EXE_PATH = ""  #C:\\Users\\User\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\\latex.exe'


def gpt(prompt):
    
    openai.api_key = OPENAI_API_KEY

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0,
      max_tokens=1000,
      top_p = 1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )

    return response['choices'][0]['text'].strip()


def concat_tex(texString, response):
    
    texList = texString.split('\n')
    bodyIndex = 0
    
    for i in range(len(texList)-1, 0, -1):
        if texList[i] == '\\section{Lecture}':
            bodyIndex = i
            break
            
    texList = texList[0:i+1] + [response] + texList[i+1:]
    texString = '\n'.join(texList)
    
    return texString


def compile_tex(texString):
    
    f = open("gpt.tex", "w")
    f.write(texString)
    f.close()
    
    process = subprocess.Popen([
        LATEX_EXE_PATH,
        '-output-format=pdf',
        '-job-name=' + 'gpt',
        'gpt.tex'])
    process.wait()  


def main():
    
    mainTex = open('template/main.tex').read()
    
    askUser = input('What subject should I teach: ')
    askUser = askUser + '. Please write the equations in LaTeX format'
    
    response = gpt(askUser)    
    
    lectureTex = concat_tex(mainTex, response)
    compile_tex(lectureTex)
    
    [os.remove(i) for i in os.listdir('./') if 'gpt' in i and 'pdf' not in i]
    
    
if __name__ == '__main__':
    main()