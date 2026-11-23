from collections import deque
import math

from flask import Blueprint, render_template, request, session

labs_bp = Blueprint("labs", __name__)


class _BSTNode:

  def __init__(self, value):
    self.value = value
    self.left = None
    self.right = None


class BinarySearchTree:

  def __init__(self):
    self.root = None

  def insert(self, node, value):
    if node is None:
      return _BSTNode(value)
    if value < node.value:
      node.left = self.insert(node.left, value)
    elif value > node.value:
      node.right = self.insert(node.right, value)
    return node

  def search(self, node, value):
    if node is None:
      return False
    if node.value == value:
      return True
    if value < node.value:
      return self.search(node.left, value)
    return self.search(node.right, value)

  def _min_node(self, node):
    current = node
    while current.left is not None:
      current = current.left
    return current

  def delete_node(self, node, value):
    if node is None:
      return None
    if value < node.value:
      node.left = self.delete_node(node.left, value)
    elif value > node.value:
      node.right = self.delete_node(node.right, value)
    else:
      if node.left is None:
        return node.right
      if node.right is None:
        return node.left
      successor = self._min_node(node.right)
      node.value = successor.value
      node.right = self.delete_node(node.right, successor.value)
    return node

  def post_traversal(self, node):
    if node is None:
      return []
    return (
        self.post_traversal(node.left)
        + self.post_traversal(node.right)
        + [node.value]
    )


def selection_sort_max(arr):
  data = list(arr)
  length = len(data)
  steps = []

  for i in range(length - 1, 0, -1):
    max_idx = 0

    for j in range(1, i + 1):
      if data[j] > data[max_idx]:
        max_idx = j

    swapped = False
    if max_idx != i:
      data[i], data[max_idx] = data[max_idx], data[i]
      swapped = True

    steps.append({
        "pass_index": i,
        "max_value": data[i] if swapped else data[max_idx],
        "swapped": swapped,
        "array_state": list(data),
    })

  return data, steps


@labs_bp.route("/works/circle", methods=["GET", "POST"])
def circle_tool():
  result = None
  error = None
  if request.method == "POST":
    try:
      r_raw = request.form.get("radius", "").strip()
      r = float(r_raw)
      if r < 0:
        raise ValueError("Radius must be non-negative.")
      result = round(math.pi * (r**2), 4)
    except ValueError as e:
      error = str(e)
  return render_template("labs/circle.html", result=result, error=error)


@labs_bp.route("/works/triangle", methods=["GET", "POST"])
def triangle_tool():
  result = None
  error = None
  if request.method == "POST":
    try:
      b_raw = request.form.get("base", "").strip()
      h_raw = request.form.get("height", "").strip()
      b = float(b_raw)
      h = float(h_raw)
      if b < 0 or h < 0:
        raise ValueError("Base and height must be non-negative.")
      result = round(0.5 * b * h, 4)
    except ValueError as e:
      error = str(e)
  return render_template("labs/triangle.html", result=result, error=error)


def to_upper(text: str) -> str:
  return text.upper()


def to_lower(text: str) -> str:
  return text.lower()


@labs_bp.route("/works/touppercase", methods=["GET", "POST"])
def touppercase():
  result = None
  text = ""
  if request.method == "POST":
    text = request.form.get("text", "")
    mode = request.form.get("mode", "upper")
    result = to_upper(text) if mode == "upper" else to_lower(text)
  return render_template("labs/touppercase.html", text=text, result=result)


@labs_bp.route("/works/linkedlist", methods=["GET", "POST"])
def linkedlist_tool():
  if "linked_list" not in session:
    session["linked_list"] = []

  message = None
  error = None

  if request.method == "POST":
    action = request.form.get("action")
    value = request.form.get("value", "").strip()
    ll = list(session["linked_list"])

    if action == "clear":
      session["linked_list"] = []
      message = "Linked list has been cleared."
    elif not value:
      error = "Please provide a node value."
    elif action == "append":
      ll.append(value)
      session["linked_list"] = ll
      message = f"Appended '{value}' to the list."
    elif action == "prepend":
      ll.insert(0, value)
      session["linked_list"] = ll
      message = f"Prepended '{value}' to the list."
    elif action == "delete":
      if value in ll:
        ll.remove(value)
        session["linked_list"] = ll
        message = f"Deleted first occurrence of '{value}' from the list."
      else:
        error = f"Value '{value}' not found in the list."

  return render_template("labs/linkedlist.html",ll=session.get("linked_list", []),
      message=message,
      error=error,
  )


@labs_bp.route("/works/infixpostfix", methods=["GET", "POST"])
def infixpostfix_tool():
  result = None
  expression = None

  if request.method == "POST":
    expression = request.form.get("expression", "").strip()
    try:
      precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
      output = []
      stack = []

      i = 0
      while i < len(expression):
        char = expression[i]
        if char.isspace():
          i += 1
          continue
        if char.isalnum():
          operand = []
          while i < len(expression) and (
              expression[i].isalnum() or expression[i] == "_"
          ):
            operand.append(expression[i])
            i += 1
          output.append("".join(operand))
          continue
        elif char == "(":
          stack.append(char)
        elif char == ")":
          while stack and stack[-1] != "(":
            output.append(stack.pop())
          if stack and stack[-1] == "(":
            stack.pop()
          else:
            raise ValueError("Mismatched parentheses in expression.")
        elif char in precedence:
          while stack and stack[-1] in precedence and (
              (char != "^" and precedence[char] <= precedence[stack[-1]])
              or (char == "^" and precedence[char] < precedence[stack[-1]])
          ):
            output.append(stack.pop())
          stack.append(char)
        else:
          raise ValueError(f"Invalid character in expression: '{char}'")
        i += 1

      while stack:
        if stack[-1] == "(":
          raise ValueError("Mismatched parentheses in expression.")
        output.append(stack.pop())

      result = "".join(output)
    except Exception as e:
      result = f"Error: {str(e)}"

  return render_template(
      "labs/infixpostfix.html", result=result, expression=expression
  )


@labs_bp.route("/works/Queue", methods=["GET", "POST"])
def queue_tool():
  if "queue" not in session:
    session["queue"] = []

  q = deque(session["queue"])
  message = None

  if request.method == "POST":
    action = request.form.get("action")
    value = request.form.get("value", "").strip()

    if action == "enqueue_rear":
      if value:
        q.append(value)
        message = f"Added '{value}' to the rear."
      else:
        message = "Please enter a value."

    elif action == "enqueue_front":
      if value:
        q.appendleft(value)
        message = f"Added '{value}' to the front."
      else:
        message = "Please enter a value."

    elif action == "dequeue_front":
      if len(q) > 0:
        removed = q.popleft()
        message = f"Removed '{removed}' from the front."
      else:
        message = "Deque is empty! Cannot remove from front."

    elif action == "dequeue_rear":
      if len(q) > 0:
        removed = q.pop()
        message = f"Removed '{removed}' from the rear."
      else:
        message = "Deque is empty! Cannot remove from rear."

    session["queue"] = list(q)

  return render_template("labs/queue.html", queue_items=list(q), message=message)


@labs_bp.route("/works/binary_tree", methods=["GET", "POST"])
def binary_tree_tool():
  if "bst_nodes" not in session:
    session["bst_nodes"] = []

  bst = BinarySearchTree()
  for val in session["bst_nodes"]:
    bst.root = bst.insert(bst.root, val)

  message = None

  if request.method == "POST":
    action = request.form.get("action")
    value = request.form.get("value", "").strip()
    nodes = list(session["bst_nodes"])

    if action == "insert":
      if value:
        bst.root = bst.insert(bst.root, value)
        if value not in nodes:
          nodes.append(value)
          session["bst_nodes"] = nodes
        message = f"Inserted node '{value}'."
      else:
        message = "Please enter a value to insert."

    elif action == "search":
      if value:
        found = bst.search(bst.root, value)
        message = (
            f"Node '{value}' found in the tree!"
            if found
            else f"Node '{value}' NOT found in the tree."
        )
      else:
        message = "Please enter a value to search."

    elif action == "delete":
      if value:
        if value in nodes:
          bst.root = bst.delete_node(bst.root, value)
          nodes.remove(value)
          session["bst_nodes"] = nodes
          message = f"Deleted node '{value}'."
        else:
          message = f"Node '{value}' not found in the tree."
      else:
        message = "Please enter a value to delete."

    elif action == "traverse":
      message = "Computed post-order traversal!"

  traversal_items = bst.post_traversal(bst.root)
  return render_template(
      "labs/binary_tree.html", traversal_items=traversal_items, message=message
  )


@labs_bp.route("/works/sorting", methods=["GET", "POST"])
def sorting_tool():
  raw_input = ""
  sorted_list = None
  steps = []
  error = None

  if request.method == "POST":
    raw_input = request.form.get("numbers", "").strip()
    try:
      numbers = [int(x.strip()) for x in raw_input.split(",") if x.strip()]
      if not numbers:
        error = "Please enter at least one number."
      else:
        sorted_list, steps = selection_sort_max(numbers)
    except ValueError:
      error = "Invalid input. Enter whole numbers separated by commas."

  return render_template(
      "labs/sorting.html",
      raw_input=raw_input,
      sorted_list=sorted_list,
      steps=steps,
      error=error,
  )

#https://csvistool.com/SelectionSort <-- here is the source pseudocode of the sorting method :3