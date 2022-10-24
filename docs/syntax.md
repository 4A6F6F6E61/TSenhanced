# Syntax

## Loops

### Forloops

```F#
let result = []
for let i = 0; i < count; i++ do
    result.push(i)
end
```

### Whileloops

```F#
while true do
    printf("Infinity")
end
```

## Conditions

```F#
let test = 1

if test == 1 then
    printf(1)
elif test == 2 then
    printf(2)
else then
    printf("else")
end
```

## CLasses

This is a simple Counter example class:

```F#
class Counter do
    private _count: int
    public constructor(public start: number) do
        this._count = start
    end

    public pp(): void do
        this._count = this._count + 1
    end

    public mm(): void do
        this._count = this._count - 1
    end

    public get count(): int do
        return this._count
    end

    public set count(value: int) do
        this._count = value
    end
end
```

## Functions

### Arrow functions

```F#
function test = (): void begin
    let t: Counter = new Counter(10)
    t.pp()
    printf(t.count)
end
```

### Normal functions

```F#
function! range (count: number): Array<number> do
    let result: Array<number> = []

    for let i = 0; i < count; i++ do
        result.push(i)
    end

    return result
end
```
