# Code Feel Examples

The following are not set in stone, but likely code to narrow down exact grammar and syntax.

## Grammar
```
<program> = <statement> [ <statement> ... ]
<statement> = (<print_statement> | <assignment>) "\n"
<print_statement> = "print" <expression>
<assignment> = identifier "=" <expression>
<expression> = number | identifier
```

## Hello World
```Chimerik
trooden("Hello world!")
```

## Input
todo

## Variable ++/--
```Chimerik
iml.int counter = 0;
counter.ap
// counter == 1
counter.dek
// counter == 0
```

## Error
```Chimerik
ston.string Greeting = "Hello"
Greeting += " world";
// melem
```

## Function
```Chimerik
drovok ston.sum(ston.x, ston.y) {
    goiims (x + y)
}
```

## Truthyness
```Chimerik
0 == viseld == long
1 == trigus == laa
2 == alo x= 3
```

## Types
```Chimerik
10 ~= 26 == trigus     // ~= true if types match
"test" ~= 26 == viseld
10 x= 26 == trigus     // x= is != (not equal)
```