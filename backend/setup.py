from setuptools import setup, find_packages

setup(
    name='MultiverseNoteBackend',  # Replace with your project name
    version='0.0.1',  # The current project version
    author='AierLab',  # Replace with your name
    author_email='hobart.yang@qq.com',  # Replace with your email
    description='MultiverseNote: Transforming AI chatbot interactions into structured project management workflows for enhanced knowledge and conversation continuity.',  # Provide a short description
    long_description=open('README.md').read(),  # This will read your README file
    long_description_content_type='text/markdown',  # This is the content type of the long description
    url='https://github.com/aierlab/multiversenote',  # Replace with the URL to your project
    packages=find_packages(),  # Automatically find all packages in your project
    include_package_data=True,  # Include other files specified in MANIFEST.in
    install_requires=[
        'flask>=2.2.3',  # Flask version
        'faiss-cpu>=1.7.3',  # FAISS CPU version
        'numpy>=1.24.3',  # Numpy version
        'openai>=0.27.0',  # OpenAI Python client version
        'requests',
        'beautifulsoup4>=4.9.3',
        'pyyaml'
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',  # Testing library
            'flake8>=4.0.0',  # Code style checker
        ],
        'test': [
            'pytest>=7.0.0',
            'coverage>=6.0',  # Code coverage tool
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',  # Project maturity
        'Intended Audience :: Developers',  # Define your audience
        'Natural Language :: English',
        'Programming Language :: Python :: 3',  # Specify which python versions you support
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',  # Minimum version requirement of Python
    entry_points={
        'console_scripts': [
            'start=app.server:main',  # This enables command-line execution
        ],
    },
)
