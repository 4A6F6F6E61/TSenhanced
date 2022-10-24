# TSenhanced

Alternate Syntax for Typescript.

## Syntax

1. [Loops](docs/syntax.md#loops)
    1. [For](docs/syntax.md#forloops)
    2. [While](docs/syntax.md#whileloops)
2. [Conditions](docs/syntax.md#conditions)
3. [Classes](docs/syntax.md#classes)
4. [Functions](docs/syntax.md#functions)
    1. [Arrowfunctions](docs/syntax.md#arrow-functions)
    2. [Normal functions](docs/syntax.md#normal-functions)

## Compile

### Compile files in directory to TypeScript

```bash
./main.py -d [directory]
```

### Compile files in directory to JavaScript (not implemented)

```bash
./main.py -j [directory]
```

## Compile and execute

### Single File with Deno

```bash
./main.py -f [file]
```

### Single File with Bun

```bash
./main.py -f [file] -bun
```

### All files in directory with Deno

```bash
./main.py -a [directory]
```

### All files in directory with Bun

```bash
./main.py -a [directory] -bun
```

Default file is `index.tsa`
