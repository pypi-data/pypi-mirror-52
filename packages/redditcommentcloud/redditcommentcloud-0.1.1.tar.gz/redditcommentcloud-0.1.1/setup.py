from distutils.core import setup
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
  name='redditcommentcloud',
  packages=['redditcommentcloud'],
  version='0.1.1',
  license='GPLv3',
  description='Python3.7+ wrapper for generating word clouds from a Reddit user\'s comments.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='Christoph Meyer',
  author_email='christoph@chmey.com',
  url='https://github.com/chmey/reddit-comment-cloud',
  keywords=['reddit', 'wordcloud'],
  install_requires=[
          'matplotlib',
          'praw',
          'WordCloud',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3'
  ],
  python_requires='>=3',
)
