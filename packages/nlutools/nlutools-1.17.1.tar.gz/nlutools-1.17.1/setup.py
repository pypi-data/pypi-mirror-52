from setuptools import setup, find_packages
import io

setup(name='nlutools',\
        version='1.17.1',\
        description='fix some return problems; add namener;',\
        #long_description=open('README.md',encoding='utf-8').read(),\
        long_description=io.open('README.md','r',-1,'utf-8').read(),\
        long_description_content_type="text/markdown",\
        url='https://github.com',\
        author='LH19880520',\
        author_email='huan.liu@ifchange.com',\
        license='ifchange',\
        install_requires=['requests>=2.18.4','bert-serving-client==1.9.6','pyzmq>=17.1.2'],\
        packages=find_packages(),\
        include_package_data=True,\
        zip_safe=False)
