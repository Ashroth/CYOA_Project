let player = {
    "Status": {"Health": 1},
    "Item": {},
    "Hidden": {}
};

let conditions = [];

function item_handler(inventory_name, item)
{
    let output_text = "";
    if (player[inventory_name].hasOwnProperty(item.name))
    {
        player[inventory_name][item.name] += item.amount;
    }
    else
    {
        player[inventory_name][item.name] = item.amount;
    }
    let too_many = false;
    if (player[inventory_name][item.name] < 0)
    {
        player[inventory_name][item.name] == 0;
        too_many = True;
    }
    if (item.type != "Hidden" && !item.hidden)
    {
        if (item.amount > 0)
        {
            output_text += `<b>Gained ${item.amount} ${item.name}</b> \n`;
        }
        else if (item.amount < 0)
        {
            if (too_many)
            {
                output_text += `You have lost all of your ${item.name} \n`;
            }
            else
            {
                output_text += `Lost ${item.amount} ${item.name} \n`;
            }
        }
    }
    return output_text
}

function conditional_adventure(index, event_id)
{
    let condition = conditions[index]
    let message = "";
    for (j in condition)
    {
        if (condition[j].amount = 0)
        {
            message = `Lost all of your ${condition.name}\n`;
            player[condition[j].type][condition[j].name] = 0;
        }
        else if (condition[j].amount < 0)
        {
            player[condition[j].type][condition[j].name] += condition[j].amount;
            message = `Lost ${condition.amount} ${condition.name}\n`;
        }
    }
    // ToDo: Message handling
    adventure(event_id);
}

function condition_checker(condition)
{
    console.log(condition);
    if (!player[condition.type].hasOwnProperty(condition.name))
    {
        return [false, "You are missing something"];
    }
    else
    {
        let message = ""
        if (condition.type == "Item")
        {
            message == `You need ${condition.amount} ${condition.name}\n`
        }
        else if (condition.type == "Status")
        {
            message = `You are too weary to attempt this (${condition.amount} ${condition.name} required)\n`
        }
        else if (condition.type == "Hidden")
        {
            message = "Something is missing\n"
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
        title.innerHTML = `<h3>${response.title}</h3>`;
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
                console.log(choice);
                let choice_element = document.createElement('button');
                if (choice[2].length > 0)
                {
                    conditions[i] = choice[2];
                    console.log(conditions[i]);
                    let open = true;
                    let variables = [];
                    let content = "";
                    for (condition in choice[2])
                    {
                        variables = condition_checker(choice[2][condition]);
                        if (!variables[0])
                        {
                            open = false;
                            content += variables[1];
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
            text.append("You have failed in your quest! \n");
            text.append(ending);
        }
        else
        {
            let ending = document.createElement('button');
            ending.setAttribute('onclick', 'location.reload()');
            ending.innerHTML = "Return to start";
            text.append("This is the end of your path. Start over?");
            text.innerHTML += "<br>"
            text.append(ending);
        }
    });
}