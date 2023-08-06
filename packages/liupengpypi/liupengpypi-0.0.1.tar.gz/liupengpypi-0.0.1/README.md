# pypi-demo
A sample demo project Packaging and distributing projects to Pypi

Packaging

```
python setup.py sdist 
```

Testing

```
pip install dist/liupengpypi-0.0.1.tar.gz 
```

```
demo
```

Distributing

```
pip install twine

twine upload dist/liupengpypi-0.0.1.tar.gz 
```
