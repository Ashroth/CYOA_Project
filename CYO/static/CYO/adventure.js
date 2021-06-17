let player = {
    "Status": {"Health": 1},
    "Item": {},
    "Hidden": {}
};

let conditions = [];
function inventory(type)
{
    const stat = document.querySelector('#text_' + type)
    stat.innerText = ""
    for (let key in player[type])
    {
        stat.innerHTML += key +': (' + player[type][key] + ")<br>";
    }
    if (stat.innerText == "")
    {
        stat.style.display = 'none';
    }
    else
    {
        stat.style.display = 'block';
    }
}

function show(type)
{
    const main = document.querySelector("#main_view");
    const side = document.querySelector('#' + type);
    const button = document.querySelector("#" + type + "_button");
    let other_button = null;
    if (type == "Item")
    {
        other_button = document.querySelector("#Status_button");
    }
    else
    {
        other_button = document.querySelector("#Item_button");
    }
    if (main.style.display == 'none')
    {
        other_button.style.display = 'inline';
        button.innerHTML = type;
        main.style.display = 'block';
        side.style.display = 'none';
    }
    else
    {
        other_button.style.display = 'none';
        button.innerHTML = "Back";
        main.style.display = 'none';
        inventory(type);
        side.style.display = 'inline';
    }
}

function item_handler(inventory_name, item)
{
    let output_text = "";
    if (player[inventory_name].hasOwnProperty(item.name))
    {
        if (item.amount != 0)
        {
            player[inventory_name][item.name] += item.amount;
        }
        else
        {
            player[inventory_name][item.name] = 0;
        }
    }
    else
    {
        if (item.amount != 0)
        {
            player[inventory_name][item.name] = item.amount;
        }
        else
        {
            player[inventory_name][item.name] = 0;
        }
    }
    let too_many = false;
    if (player[inventory_name][item.name] < 0)
    {
        player[inventory_name][item.name] = 0;
        too_many = true;
    }
    if (item.type != "Hidden" && !item.hidden)
    {
        if (item.amount > 0)
        {
            output_text += `<b>Gained ${item.amount} ${item.name}</b> <br>`;
        }
        else if (item.amount < 0)
        {
            if (too_many)
            {
                output_text += `You have lost all of your ${item.name} <br>`;
            }
            else
            {
                output_text += `Lost ${item.amount} ${item.name} <br>`;
            }
        }
        else
        {
            output_text += `You have lost all of your ${item.name} <br>`;
        }
    }
    return output_text
}

function conditional_adventure(index, event_id)
{
    let condition = conditions[index]
    for (j in condition)
    {
        if (condition[j].amount == 0)
        {
            player[condition[j].type][condition[j].name] = 0;
        }
        else if (condition[j].amount < 0)
        {
            player[condition[j].type][condition[j].name] += condition[j].amount;
        }
    }
    adventure(event_id);
}

function condition_checker(condition)
{
    if (!player[condition.type].hasOwnProperty(condition.name))
    {
        return [false, "You are missing something"];
    }
    else
    {
        let message = ""
        if (condition.type == "Item")
        {
            message = `You need ${Math.abs(condition.amount)} ${condition.name}<br>`
        }
        else if (condition.type == "Status")
        {
            message = `You are too weary to attempt this (${condition.amount} ${condition.name} required)<br>`
        }
        else if (condition.type == "Hidden")
        {
            message = "Something is missing<br>"
        }
        if (player[condition.type][condition.name] < condition.amount || player[condition.type][condition.name] + condition.amount < 0)
        {
            return [false, message];
        }
        else
        {
            return [true, ""];
        }
    }
}

function adventure(event_id)
{
    fetch(`event/${event_id}`,{
        method: 'GET'
    })
    .then((response) => response.json())
    .then((response) => {
        if (response.status == 404)
        {
            return null;
        }
        let title = document.querySelector("#title");
        let text = document.querySelector("#text");
        title.innerHTML = `<h2>${response.title}</h2>`;
        text.innerHTML = response.text;
        text.innerHTML += "<br>"
        for (j in response.items)
        {
            let item = response.items[j];
            if (item.type == "Item")
            {
                text.innerHTML += item_handler("Item", item);
            }
            else if (item.type == "Status")
            {
                text.innerHTML += item_handler("Status", item);
            }
            else if (item.type == "Hidden")
            {
                text.innerHTML += item_handler("Hidden", item);
            }
        }
        if (player.Status.Health > 0 && response.choices.length > 0)
        {
            conditions = [];
            for (i in response.choices)
            {
                let choice = response.choices[i]
                let choice_element = document.createElement('button');
                if (choice[2].length > 0)
                {
                    conditions[i] = choice[2];
                    let open = true;
                    let variables = [];
                    let content = "";
                    for (condition in choice[2])
                    {
                        variables = condition_checker(choice[2][condition]);
                        if (!variables[0])
                        {
                            open = false;
                            content += variables[1] + " ";
                        }
                    } 
                    if (open)
                    {
                        choice_element.setAttribute('onclick', `conditional_adventure(${i}, '${choice[0]}')`);
                        choice_element.innerHTML = choice[1];
                    }
                    else
                    {
                        choice_element.style.textEmphasisColor = "gray";
                        choice_element.innerHTML = content;
                    }
                }
                else
                {
                    choice_element.setAttribute('onclick', `adventure('${choice[0]}')`);
                    choice_element.innerHTML = choice[1];
                }
                text.append(choice_element)
            }
        }
        else if (player.Status.Health == 0)
        {
            let ending = document.createElement('button');
            ending.setAttribute('onclick', 'location.reload()');
            ending.innerHTML = "Return to start";
            text.append("You have failed in your quest!");
            text.innerHTML += "<br>"
            text.append(ending);
        }
        else
        {
            let ending = document.createElement('button');
            ending.setAttribute('onclick', 'location.reload()');
            ending.innerHTML = "Return to start";
            text.append("This is the end of your path. Start over?");
            text.innerHTML += "<br>";
            text.append(ending);
        }
    });
}