from setuptools import setup

setup(name='wordcutpy',
      version='0.1.1',
      description='Thai word tokenizer written in Python',
      url='https://github.com/veer66/wordcutpy.git',
      author='Vee Satayamas',
      author_email='vsatayamas@gmail.com',
      license='LGPLv3',
      package_data={'': ['LICENSE', 'LICENSE-DICT', 'README.md', 'bigthai.txt', 'dict.txt']},
      include_package_data=True,
      packages=['wordcut'],
      zip_safe=False)
