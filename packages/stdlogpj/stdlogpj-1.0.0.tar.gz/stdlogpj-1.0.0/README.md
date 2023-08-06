# stdlogpj
python logging done my way

home: https://github.com/prjemian/stdlogpj

INSTALL

    conda install -c aps-anl-tag stdlogpj
    conda install -c prjemian stdlogpj
    pip install stdlogpj

USAGE:

    import stdlogpj
    logger = stdlogpj.standard_logging_setup("demo")
    logger.info("hello")

DEMO:

```python
#!/usr/bin/env python

import stdlogpj

logger = stdlogpj.standard_logging_setup("stdlogpj-demo")


def thing1(i):
    logger.info(f"something #{i+1}")


def main():
    logger.info("hello")
    for i in range(5):
        logger.debug("calling thing1()")
        thing1(i)
    logger.critical("complete")


if __name__ == "__main__":
    logger.warning("before main()")
    main()
    logger.error("after main(): no error, really")
```
