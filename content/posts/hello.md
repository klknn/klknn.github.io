---
title: "Markdown examples"
date: 2020-07-07T14:24:12+09:00
draft: false
tags: ["hugo", "lang-en"]
isCJKLanguage: false
---

## footnote

hello[^a]

[^a]: this is footnote

![emacs-company-dcd.png](/emacs-company-dcd.png)

{{< figure src="/emacs-company-dcd.png" caption="caption for image." >}}


## code block
```python
def f(x):
	return x * x
```

## math
\begin{align}
\label{eq:sample}
f(x) = x^2
\end{align}

## table

| aaaaaaaa | bb | c |
|:---------|--:|--:|
| 1        | 2 | 3 |
| 4        | 5 | 6 |



Eq. \eqref{eq:sample} $x^2$

## list

1. aaa
2. bb

- aaaaaaaa
- bbbb
