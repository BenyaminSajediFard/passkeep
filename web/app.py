import sys
from flask import Flask, render_template, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash

from models.users import UserModel
from models.connection import ConnectionModel
from resources.users import create_users_table

app = Flask(__name__)
is_signed_in = False

# TODO use separate URI handlers
@app.route("/")
def load_home():
    return render_template("index.html")


@app.route("/sign-up")
def load_signup():
    create_users_table()
    return render_template("sign-up.html")


@app.route("/sign-in")
def load_signin():
    create_users_table()
    return render_template("sign-in.html")


@app.route("/<string:username>/sgn-ot")
def sign_out_action(username: str):
    global is_signed_in
    if is_signed_in:
        is_signed_in = False
        return render_template(
            "showcase.html",
            result={
                "title": "Hope to see you soon! 👋",
                "content": "You were signed out of your passkeep successfully.",
                "link": None,
                "link-text": "Passkeep Main Page 🔐",
                "link": f"http://127.0.0.1:8081/",
            },
        )
    return "not signed in"


@app.route("/rgt-rs", methods=["GET", "POST"])
def register_action():
    if request.method == "POST":
        data = request.form.to_dict()
        if (passwd := data["password-original"]) == data["password-confirm"] and len(
            passwd
        ) >= 8:
            if user := UserModel.find_by_username(data["username"].casefold()):
                return render_template(
                    "showcase.html",
                    result={
                        "title": "It seems like we've met before! 🤔",
                        "content": f"Hey {user.username}, you already have an account in the database.",
                        "link": "http://127.0.0.1:8081/sign-in",
                    },
                )
            password = generate_password_hash(passwd)
            user = UserModel(data["username"].casefold(), password)
            user.create_user()
            return render_template(
                "showcase.html",
                result={
                    "title": "Registration was successful! 🥳",
                    "content": "Easy as that & now you can sign in and enjoy passkeep features...",
                    "link": "http://127.0.0.1:8081/sign-in",
                    "redirect": f"http://127.0.0.1:8081/sign-in",
                    "timeout": "2",
                },
            )
        else:
            return render_template(
                "showcase.html",
                result={
                    "title": "It might just be a TYPO! 😮‍💨",
                    "content": "looks like the passwords you entered does not match or is too short. would you mind trying again?!",
                    "link": "http://127.0.0.1:8081/sign-up",
                },
            )
    else:
        return render_template(
            "showcase.html",
            result={
                "title": "OH NO! 😨",
                "content": "looks like something(s) went wrong. Try again later...?!",
                "link": "#",
            },
        )


@app.route("/sgn-rs", methods=["GET", "POST"])
def signin_action():
    if request.method == "POST":
        data = request.form.to_dict()
        if user := UserModel.find_by_username(data["username"].casefold()):
            if check_password_hash(user.password, data["password"]):
                global is_signed_in
                if is_signed_in:
                    return render_template(
                        "showcase.html",
                        result={
                            "title": "Hey, You are in already 🙄",
                            "content": "Looks like you have already signed into the system, so I'll redirect you to the home...",
                            "redirect": f"http://127.0.0.1:8081/{user.username}/home",
                            "timeout": "2",
                        },
                    )
                is_signed_in = True
                return render_template(
                    "showcase.html",
                    result={
                        "user": user.username,
                        "title": f"Hey {user.username}, welcome back! 😄",
                        "content": """Log in to your passkeep was successful.
                        we will redirect you to home panel in 3 seconds...""",
                        # TODO: add a timer (as final touches!)
                        "link-text": "Go to panel homepage 🏠",
                        "link": f"http://127.0.0.1:8081/{user.username}/home",
                        "redirect": f"http://127.0.0.1:8081/{user.username}/home",
                        "timeout": "2",
                    },
                )
            return render_template(
                "showcase.html",
                result={
                    "title": "OOPS! 😵",
                    "content": "Password doesn't seem to match with the one we have... wanna try again?",
                    "link": "http://127.0.0.1:8081/sign-in",
                },
            )
        return render_template(
            "showcase.html",
            result={
                "title": "Let's meet each other 🤗",
                "content": "Our database tells me that it doesn't know you (yet!) let's fix that now by pressing `continue` link below.",
                "link": "http://127.0.0.1:8081/sign-up",
                "redirect": f"http://127.0.0.1:8081/sign-up",
                "timeout": "2",
            },
        )
    else:
        return render_template(
            "showcase.html",
            result={
                "title": "OH NO! 😨",
                "content": "looks like something(s) went wrong. Try again later...?!",
                "link": "#",
            },
        )


@app.route("/<string:username>")
def user_page(username):
    if is_signed_in:
        return redirect(f"/{username}/home")
    else:
        return render_template("sign-in.html", user=username)


@app.route("/<string:username>/home")
def user_panel(username="dummy"):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            connection = ConnectionModel(user)
            all_data = connection.select_data()
            connection.close_connection()
            return render_template(
                "app.html",
                result={
                    "username": user.username,
                    "data": all_data,
                    "row": None,
                    "link": f"http://127.0.0.1:8081/{username}/",
                },
                content=None,
            )
        return "user was not found"
    else:
        return "not signed in"


@app.route("/<string:username>/home/<int:data_id>")
def load_selected(username="dummy", data_id=1):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            connection = ConnectionModel(user)
            all_data = connection.select_data()
            if item := [item for item in all_data if item[0] == data_id]:
                item_id, item_source, item_password = item[0]
                item_url = f"http://127.0.0.1:8081/{username}/home/{item_id}"
                active_item = (item_id, item_source, item_password, item_url)
                connection.close_connection()
                return render_template(
                    "app.html",
                    result={
                        "username": user.username,
                        "data": all_data,
                        "link": f"http://127.0.0.1:8081/{username}/",
                    },
                    item=item_id,
                    content=active_item,
                )
            else:
                connection.close_connection()
                return render_template("no matching item was found")
        else:
            return "user was not found"
    else:
        return "not signed in"


# PASSWORD GENERATION ENDPOINTS
@app.route("/<string:username>/gen-pass")
def password_generator(username: str):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            return render_template("new-action.html", user=user.username)
        return "user was not found"
    else:
        return "not signed in"


@app.route("/<string:username>/new-entry", methods=["GET", "POST"])
def generator_result(username: str):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            if request.method == "POST":
                from utils.pass_generator import assemble_passwd

                data = request.form.to_dict()
                source, pass_level = data["source"].casefold(), data["pass-level"]

                connection = ConnectionModel(user)
                if bool(connection.select_data("source", source)):
                    return render_template(
                        "showcase.html",
                        result={
                            "title": "No duplicate rule 👬",
                            "content": f"We found another source with the same value as {source}. so go ahead and change that please...",
                            "redirect": f"http://127.0.0.1:8081/{user.username}/gen-pass",
                            "timeout": "2",
                            "link": None,
                        },
                    )
                new_password = assemble_passwd(pass_level)

                connection.insert_data(source, new_password)
                connection.close_connection()

                return render_template(
                    "showcase.html",
                    result={
                        "title": "New entry added! 👍",
                        "content": f"A new password for {source} was generated successfully.",
                        "redirect": f"http://127.0.0.1:8081/{user.username}/home",
                        "timeout": "2",
                        "link": None,
                    },
                )
        return "user was not found"
    return "not signed in"


# PASSWORD SEARCH ENDPOINT
@app.route("/<string:username>/se-term")
def search_item(username: str):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            return render_template("se-action.html", user=user.username)
        return "user was not found"
    return "not signed in"


@app.route("/<string:username>/home/result", methods=["GET", "POST"])
def search_result(username):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            if request.method == "POST":
                data = request.form.to_dict()
                search_term, search_param = (
                    data["term"],
                    data["search-param"],
                )
                print(data)

                connection = ConnectionModel(user)
                all_data = connection.select_data()
                if search_param == "id":
                    result = next(
                        filter(lambda x: int(search_term) == x[0], all_data), None
                    )
                elif search_param == "source":
                    result = next(
                        filter(lambda x: search_term.casefold() in x[1], all_data), None
                    )
                else:
                    result = next(filter(lambda x: search_term in x[2], all_data), None)
                print(result)
                if result:
                    return redirect(
                        f"http://127.0.0.1:8081/{username}/home/{result[0]}"
                    )
                return "item not found"
        return "user was not found"
    return "not signed in"


# PASSWORD EDIT ENDPOINTS
@app.route("/<string:username>/ed-id<int:data_id>")
def edit_data(username: str, data_id: int):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            connection = ConnectionModel(user)
            all_data = connection.select_data()
            connection.close_connection()
            if item := [item for item in all_data if item[0] == data_id]:
                item_id, item_source, item_password = item[0]
                return render_template(
                    "edit-action.html",
                    content={
                        "source": item_source,
                        "password": item_password,
                        "id": data_id,
                    },
                )
            return "no such item id was found"
        return "user was not found"
    return "not signed in"


@app.route("/<string:username>/edited", methods=["GET", "POST"])
def edit_result(username: str):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            if request.method == "POST":
                data = request.form.to_dict()
                item_id, new_source, new_password = (
                    data["id"],
                    data["new-source"],
                    data["new-password"],
                )

                connection = ConnectionModel(user)
                connection.edit_data(item_id, new_source, new_password)
                connection.close_connection()
                return render_template(
                    "showcase.html",
                    result={
                        "title": "Edited... or is it?! 🤥",
                        "content": "The selected item was edited successfully.",
                        "redirect": f"http://127.0.0.1:8081/{user.username}/home",
                        "timeout": "2",
                    },
                )
        else:
            return "user was not found"
    else:
        return "not signed in"


# PASSWORD DELETION ENDPOINTS
@app.route("/<string:username>/del-id<int:data_id>")
def confirm_deletion(username: str, data_id: int):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            connection = ConnectionModel(user)
            data = connection.select_data("id", data_id)
            connection.close_connection()
            item_id, item_source, _ = data[0]
            return render_template(
                "del-action.html", content={"source": item_source, "id": item_id}
            )
        return "user was not found"
    return "not signed in"


@app.route("/<string:username>/deleted", methods=["GET", "POST"])
def deletion_result(username: str):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            if request.method == "POST":
                user_res = tuple(request.form.to_dict().keys())[0]
                if user_res == "cancel":
                    return render_template(
                        "showcase.html",
                        result={
                            "title": "Operation got cancelled!",
                            "content": "The item's deletion was aborted. going back to home 🏡 page...",
                            "redirect": f"http://127.0.0.1:8081/{user.username}/home",
                            "timeout": "2",
                        },
                    )
                connection = ConnectionModel(user)
                connection.delete_data("id", user_res)
                connection.close_connection()
                return render_template(
                    "showcase.html",
                    result={
                        "title": "Out of sight, Out of database! 🙈",
                        "content": "The selected item was deleted successfully.",
                        "redirect": f"http://127.0.0.1:8081/{user.username}/home",
                        "timeout": "2",
                    },
                )
        return "user was not found"
    return "not signed in"


# PASSWORD CHECKER
@app.route("/<string:username>/is-pwned/<int:item_id>")
def check_by_id(username, item_id):
    if is_signed_in:
        if user := UserModel.find_by_username(username):
            from utils.pass_check import is_pawned

            connection = ConnectionModel(user)
            item_password = ""
            if data := connection.select_data("id", item_id):
                *_, item_password = data[0]
            else:
                return "no such item"

            result = is_pawned(item_password)
            if result.get("is-pwned", None):
                return render_template(
                    "showcase.html",
                    result={
                        "title": "Oh no!!! 😱",
                        "content": f"The statistics shows that your current password has been pwned for about {result['count']} times. It is advised to consider changing it ASAP.",
                        "link-text": "Go to panel homepage 🏠",
                        "link": f"http://127.0.0.1:8081/{user.username}/home",
                    },
                )
            elif result.get("err", None):
                return redirect(f"http://127.0.0.1:8081/{user.username}/home")
            return render_template(
                "showcase.html",
                result={
                    "title": "What a relief 😇",
                    "content": "Thing are looking up for now, your password was not found in the pwned database and proved to be secure.   (at least for now!)",
                    "redirect": f"http://127.0.0.1:8081/{user.username}/home",
                    "timeout": "4",
                },
            )
        return "user was not found"
    return "not signed in"


@app.route("/<string:username>/pass-checker")
def check_by_pass(username):
    return render_template("pass-check.html", user=username)


@app.route("/<string:username>/checked", methods=["GET", "POST"])
def check_result(username):
    if request.method == "POST":
        from utils.pass_check import is_pawned

        password = request.form.to_dict()["password"]
        result = is_pawned(password)
        if result.get("is-pwned", None):
            return render_template(
                "showcase.html",
                result={
                    "title": "Oh no!!! 😱",
                    "content": f"It seems that the password you entered has been pwned for about {result['count']} times. If it is in use, it would be wise to consider changing it ASAP.",
                    "link-text": "Go to panel homepage 🏠",
                    "link": f"http://127.0.0.1:8081/{username}/home",
                },
            )
        elif result.get("err", None):
            return redirect(f"http://127.0.0.1:8081/{username}/home")
        return render_template(
            "showcase.html",
            result={
                "title": "What a relief 😇",
                "content": "Thing are looking up for now, your password was not found in the pwned database and proved to be secure.   (at least for now!)",
                "redirect": f"http://127.0.0.1:8081/{username}/home",
                "timeout": "3",
            },
        )


if __name__ == "__main__":
    sys.exit(app.run(port=8081, debug=True))
