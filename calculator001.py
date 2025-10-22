"""Small, easy-to-read safe calculator.

This version keeps the same safety guarantees but uses simpler code and
more inline comments so it's easier to follow.

Usage examples:
  python calculator.py "2 + 3 * (4 - 1)"
  python calculator.py
    (then type expressions at the prompt)
"""

import ast
import sys


def _is_number(node):
    """Return the numeric value for ast.Constant/ast.Num or raise ValueError."""
    # ast.Constant is used on modern Pythons, ast.Num on very old ones
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed")
    if isinstance(node, ast.Num):
        return node.n
    raise ValueError("Expected a numeric literal")


def safe_eval(expr: str):
    """Safely evaluate a simple arithmetic expression.

    Supports +, -, *, /, %, ** and unary +/-. Rejects names, calls, etc.
    """
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}")

    def _eval(node):
        # Expression wrapper
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        # Binary operations: evaluate left and right then apply operator
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Mod):
                return left % right
            if isinstance(node.op, ast.Pow):
                return left ** right
            raise ValueError("Unsupported binary operator")

        # Unary + and -
        if isinstance(node, ast.UnaryOp):
            val = _eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +val
            if isinstance(node.op, ast.USub):
                return -val
            raise ValueError("Unsupported unary operator")

        # Numeric literal
        return _is_number(node)

    return _eval(tree)


def repl():
    print("Calculator REPL. Type 'quit' or 'exit' to leave.")
    while True:
        try:
            s = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not s:
            continue
        if s.lower() in ('quit', 'exit'):
            break

        # If the user mixes letters with the expression, reject it early
        if any(c.isalpha() for c in s):
            print('Only numbers and operators are allowed')
            continue

        try:
            result = safe_eval(s)
            print(f'Answer is: {result}')
        except SyntaxError:
            print('Invalid expression: syntax error')
        except ValueError as e:
            print('Invalid expression:', e)
        except ZeroDivisionError:
            print('Math error: division by zero')
        except Exception as e:
            print('Error:', e)

        # Ask user whether to continue
        while True:
            ans = input('Do you want another calculation? (y/n): ').strip().lower()
            if ans in ('y', 'yes'):
                break
            if ans in ('n', 'no'):
                return
            print("Please answer 'y' or 'n'.")


if __name__ == '__main__':
    # If an expression is provided as CLI args, evaluate and exit.
    if len(sys.argv) > 1:
        expr = ' '.join(sys.argv[1:])
        try:
            result = safe_eval(expr)
            print(f'Answer is: {result}')
        except Exception as e:
            print('Error:', e)
            sys.exit(1)
    else:
        # Looping prompt: evaluate each entered expression until quit
        print("Enter expressions (or press Enter to open REPL). Type 'quit' to exit.")
        while True:
            try:
                s = input('> ').strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not s:
                repl()
                break
            if s.lower() in ('quit', 'exit'):
                break

            # Reject letters in the main prompt as well
            if any(c.isalpha() for c in s):
                print('Only numbers and operators are allowed')
                continue

            try:
                result = safe_eval(s)
                print(f'Answer is: {result}')
            except SyntaxError:
                print('Invalid expression: syntax error')
            except ValueError as e:
                print('Invalid expression:', e)
            except ZeroDivisionError:
                print('Math error: division by zero')
            except Exception as e:
                print('Error:', e)

            # Ask whether the user wants another calculation
            while True:
                ans = input('Do you want another calculation? (y/n): ').strip().lower()
                if ans in ('y', 'yes'):
                    break
                if ans in ('n', 'no'):
                    sys.exit(0)
                print("Please answer 'y' or 'n'.")

