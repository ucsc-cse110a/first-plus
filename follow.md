

Great topic — this is one of the 
A confusing part of LL(1) is how to build the First+ parsing 
table.  After removing 
 a **clear, step-by-step explanation** of how a **partial FOLLOW set** is used to build a **FIRST+ set**.

---


# Big picture first

When building an **LL(1) parsing table**, each production needs a prediction set called:

> **FIRST+ (A → α)**

This tells the parser **when to use that production**.

We compute it using:

```
FIRST+ (A → α) =
    FIRST(α)           if α does NOT derive ε
    FIRST(α) ∪ FOLLOW(A)   if α CAN derive ε
```

The tricky part is:

> Where does FOLLOW(A) come from — and why do we sometimes only need a *partial* FOLLOW set?

---

# Step 1: Understand what FOLLOW(A) means

**FOLLOW(A)** = all terminals that can appear **immediately after A** in some sentential form.

Example:

```
S → A B
```

Everything in FIRST(B) (except ε) is in FOLLOW(A).

If B can derive ε:
then FOLLOW(S) also goes into FOLLOW(A).

---

# Step 2: Why FIRST+ sometimes needs only a *partial* FOLLOW

When computing FIRST+ for **one production**, we don't need the entire completed FOLLOW set for every nonterminal.

We only need:

> The FOLLOW of the left-hand side nonterminal for productions whose RHS can derive ε.

So we build FOLLOW **incrementally** — just enough to compute FIRST+.

That’s what a **partial FOLLOW set** means.

---

# Step 3: Procedure to compute FIRST+

We do this per production.

For production:

```
A → α
```

### Case 1 — α cannot derive ε

Then:

```
FIRST+(A → α) = FIRST(α)
```

No FOLLOW needed.

---

### Case 2 — α CAN derive ε

Then:

```
FIRST+(A → α) = FIRST(α) − {ε}  ∪ FOLLOW(A)
```

Now we need FOLLOW(A).

But we only compute FOLLOW(A) enough to know:

> what terminals can appear after A

This is the **partial FOLLOW** idea.

---

# Step 4: How to build the partial FOLLOW set

We compute FOLLOW using grammar rules.

### Rule 1: Start symbol

Put `$` (end marker) in FOLLOW(start symbol)

```
FOLLOW(S) = { $ }
```

---

### Rule 2: A → αBβ

Everything in FIRST(β) except ε goes into FOLLOW(B)

Example:

```
A → B C
```

Add FIRST(C) − {ε} to FOLLOW(B)

---

### Rule 3: If β can derive ε

Add FOLLOW(A) to FOLLOW(B)

Example:

```
A -> B C
C ->  ε
```

Then:

```
FOLLOW(A) gets expanded by FOLLOW(B)
  due to nullification of C

```

---

# Step 5: Why this is called “partial”

When building FIRST+ sets:

We don’t always need FOLLOW for every symbol fully solved.

We only compute FOLLOW(A) for the specific nonterminal whose production can derive ε.

So we:

1. Compute FIRST sets fully
2. Begin FOLLOW computation
3. Only propagate FOLLOW where needed
4. Stop once FIRST+ sets are known

We don’t always need the complete global FOLLOW closure first.

---

# Step 6: Full example

Grammar:

```
S → A a
S → b
A → c
A → ε
```

---

## FIRST sets

```
FIRST(A) = { c, ε }
FIRST(S → A a):
    FIRST(A a) = { c, a }
FIRST(S → b) = { b }
```

---

## FOLLOW sets (partial)

Start symbol:

```
FOLLOW(S) = { $ }
```

From:

```
S → A a
```

A is followed by `a`

So:

```
FOLLOW(A) = { a }
```

We don’t need anything else for this grammar.

---

## FIRST+ sets

### Production: S → A a

α = A a (cannot derive ε)

```
FIRST+(S → A a) = { c, a }
```

---

### Production: S → b

```
FIRST+(S → b) = { b }
```

---

### Production: A → c

```
FIRST+(A → c) = { c }
```

---

### Production: A → ε

ε-production → needs FOLLOW(A)

```
FIRST+(A → ε) = FOLLOW(A)
              = { a }
```

Here we only needed FOLLOW(A),
not full FOLLOW for entire grammar.

That’s a **partial FOLLOW** used to build FIRST+.

---

# Key insight (the core idea)

> FIRST handles what begins a production
> FOLLOW handles what can appear after it
> FIRST+ combines them to decide parsing table entries

And:

> We only compute as much FOLLOW as needed for ε-productions.

That limited computation is what people call a **partial FOLLOW set**.

---

# Short summary you can reuse

**To build FIRST+ for a production A → α:**

1. Compute FIRST(α)
2. If ε not in FIRST(α)

   * FIRST+ = FIRST(α)
3. If ε in FIRST(α)

   * FIRST+ = FIRST(α) − {ε} ∪ FOLLOW(A)
4. FOLLOW(A) only needs to be computed enough to resolve these cases
   → this is called using a *partial FOLLOW set*

---

# Want a super crisp “teaching explanation”?

I can now write this as:

* a textbook-style definition
* an exam-ready answer
* a visual diagram explanation
* or a step-by-step algorithm

Which version are you trying to create?

