import travail
import io
import setuptools

setuptools.setup(name='travail',
                 version=travail.__version__,
                 packages=['travail'],
                 install_requires=['toil>=3.20.0', 'requests>=2.22.0', 'protobuf>=3.8.0', 'pyyaml>=5.1.2'],

                 long_description=io.open('README.md', encoding='utf-8').read(),
                 long_description_content_type='text/markdown',

                 author='Daniel Danis',
                 author_email='daniel.gordon.danis@gmail.com',
                 url='https://github.com/ielis/travail',
                 description='Pipeline for processing samples in context of rare mendelian diseases',
                 license='GPLv3',
                 keywords='bioinformatics genomics mendelian disease exome genome sequencing',

                 package_data={'travail': ['utils/data/hg19.dict',
                                           'utils/data/hg38.dict']},
                 entry_points={'console_scripts': [
                     'travail = travail.main:main'
                 ]},
                 test_suite='tests')
