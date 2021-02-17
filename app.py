from flask import Flask, jsonify, redirect, send_file, request
import bill_tracker_core as core

app = Flask(__name__)

# Get config from core
CONFIG = core.CONFIG


# Add more config constants
# CONFIG.update({
#     "key": "value"
# })


# region Bill actions.
# Todo: These could be placed in Bill class, or in core file?
# Returns n in upper case
def cap(n):
    return n.upper()


# Returns n with spaces between each character.
def space(n):
    return " ".join(n)


# Returns the bill with given id in JSON form
def find_bill(id):
    bill = core.Bill(
        "Sample bill",
        "This is a sample bill: a placeholder. Probably for debugging and testing purposes.",
        "1/1/2021",
        "2/1/2022",
        "active",
        short_desc="Sample Bill"
    )
    return bill.to_dict()


def get_top_bills(range):
    bill1 = core.Bill(
        "id_1",
        "Sample bill",
        "This is a sample bill: a placeholder. Probably for debugging and testing purposes.",
        "1/1/2021",
        "2/1/2022",
        "active",
        short_desc="Sample Bill"
    )
    bill2 = core.Bill(
        "id_2",
        "Another Sample bill",
        "This is a different sample bill: an example. Probably for testing purposes.",
        "1/2/2121",
        "2/1/2122",
        "inactive",
        short_desc="Different Sample Bill"
    )

    return [bill1.to_dict(), bill2.to_dict()]


# endregion

# Mapping of "actions" (from URL) to their respective functions
# !! Any function referenced in this dict can be run by anyone !!
safe_actions = {
    "capitalise": cap,
    "space": space,
    "get": find_bill,
}


# Sample private function
# We don't want private functions to be accessible from the internet, so this function should NOT be put in the actions
#   array.
def unsafe_function(n):
    # Do something that shouldn't be accessible publicly
    print("oh dear!")


# Perform action on given bill
@app.route('/b/<bill_id>/<action>')
def handle_request(bill_id, action):
    # not case-sensitive
    action = action.lower()

    # Run requested action if valiid
    if action in safe_actions:
        result = safe_actions[action](bill_id)
    else:
        result = f"unknown or forbidden action: {action}"

    # Construct output
    output = {
        "bill_id": bill_id,
        "action": action,
        "result": result
    }

    # Convert to json and return
    return jsonify(output)


@app.route('/top')
def top():
    result = get_top_bills(10)
    # Construct output
    output = {
        "result": result
    }

    # Convert to json and return
    return jsonify(output)


@app.route('/')
def landing_page():
    return redirect(CONFIG["default_url"])


# TO MAKE IT WORK. TYPE IN THE LOGIN/USERNAME/PASSWORD and hit enter
# It will then redirect you to the logged_in or garbage page, depending on if you gave it the right password or not
@app.route('/login/<username>/<password>')  # TODO change this it is a really bad practice
def login(username, password):
    user = core.User("sg2295", "password")  # TODO fetch the actual user, no DB setup yet :(
    if user.verify_password(password):
        return redirect('/logged_in')
    else:
        return redirect('/garbage')


# Deliver requested resource.
# todo: generalise so works with filetypes other than image
@app.route(CONFIG["external_res_path"] + '<name>')
def get_res(name):
    # print(request.mimetype)
    # todo: sort out mimetype. This might affect retrieving images in the future.
    return send_file(CONFIG["img_dir"] + name)

    # return send_file("CONFIG["img_dir"] + core.CONFIG["invalid_img"], mimetype='image/gif')


# Login was successful.
@app.route('/logged_in')
def successful_login():
    return "<h1> you logged in successfully </h1> nice."


# Login failed.
@app.route('/garbage')
def garbage_page():
    return "<h1> this is a garbage page </h1> If you are here, you are garbage."


if __name__ == '__main__':
    app.run()
