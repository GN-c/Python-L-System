from PyInquirer import prompt
import turtle
from string import Template
import io
questions = [
    {
        'type': 'input',
        'name': 'axiom',
        'message': 'Enter Starting Axiom',
        # "filter":lambda a: a.upper(),
        "validate": lambda input: len(input) and all(char in ["F", "f", "B", "b", "+", "-", "[", "]"] for char in list(input)) or 'Enter valid axiom consisting of valid commands'
    },
    {
        'type': 'input',
        'name': 'angle',
        'message': 'Enter turning angle',
        "validate": lambda a: a.isnumeric() or 'invalid angle'
    },
    {
        'type': 'input',
        'name': 'evolution',
        'message': 'Enter Evolution quantity',
        "validate": lambda a: a.isnumeric() or 'invalid Evolution'
    },
    {
        'type': 'input',
        'name': 'rules',
        'message': 'Enter Rules In Format In=>Out,Seperate Rules With Commas',
        # შეიცავს "=>" ანუ მინ ერთი ბრძანებაა და სწორად არის დაწერილი
        "validate": lambda input: input.count("=>")
        # თითოეული სიმბოლო დასასშვებია და შეესაბამება რაიმე ბრძანებას
        and all(char in ["F", "f", "B", "b", "+", "-", "[", "]", ","] for char in list(",".join(input.split("=>"))))
        # თითოეულ ბრძანებაში პირველი ნაწილი-Input შედგება მხოლოდ ერთი სიმბოლოსგან და არის სწორი ცალკე მდგომი ბრძანება,outPut კი არანაკლებ 1 სიმბოლოსგან და არის მხოლოდ input და outPut
        and all(len(command) == 2 and len(command[1]) and command[0] in ["F", "f", "B", "b", "+", "-"] for command in list(map(lambda i: i.split("=>"), input.split(","))))
        # თითოეული ბრძანების მეორე ნაწილში-Output-ში თანაბარი რაოდენობის push(state-ის შემნახველი) და pop(state-ის გამხსნელი) ბრძანებაა
        and all(command[1].count("[") == command[1].count("]") for command in list(map(lambda i: i.split("=>"), input.split(","))))
        or 'invalid rules'  # მესიჯი
    },
    {
        "type": "list",
        "name": "svg",
        "message": "Do you want to export as svg?",
        "choices": ["Yes", "No"]
    }
]

print("*** Python ***")
print("*** Command Line L-Systems ***")
print("""Commands:
F => Forward
f => Forward
B => Backward
b => Backward
+ => Turn by Angle
- => Turn by Angle in opposite
[ => push
] => pop""")

answers = prompt(questions)
# print(answers)
# answers = {'axiom': 'f', 'angle': '60', 'evolution': '9',
#            'rules': 'f=>F-f-F,F=>f+F+f', 'svg': 'Yes'}

rules_dict = dict(map(lambda el: el.split("=>"), answers["rules"].split(",")))
l_string = answers["axiom"]
for _ in range(int(answers["evolution"])):
    l_string = "".join(
        map(lambda char: rules_dict.get(char, char), list(l_string)))

# Draw
if answers["svg"] == "Yes":
    svg_poses = []

t = turtle.Turtle()
turtle.tracer(False)
# t.speed(0)
stack = []
for char in l_string:
    if char == "F" or char == "f":
        if answers["svg"] == "Yes":
            svg_poses.append(t.position())
        t.forward(100/int(answers["evolution"]))
    elif char == "B" or char == "b":
        if answers["svg"] == "Yes":
            svg_poses.append(t.position())
        t.backward(100/int(answers["evolution"]))
    elif char == "-":
        t.right(int(answers["angle"]))
    elif char == "+":
        t.left(int(answers["angle"]))
    elif char == "[":
        stack.append((t.position(), t.heading()))
    elif char == "]":
        p_h = stack.pop()
        t.seth(p_h[1])
        t.setpos(p_h[0])


def mapValue(value, min, max, dMin, dMax): return (
    (value-min)/(max-min)) * (dMax-dMin) + dMin


if answers["svg"] == "Yes":
    with io.open("l-systems.svg", "w", encoding='utf8') as svg:
        svg_poses_x = list(map(lambda pos: pos[0], svg_poses))
        svg_poses_y = list(map(lambda pos: pos[1], svg_poses))
        y_min = min(svg_poses_y)
        x_min = min(svg_poses_x)
        x_max = max(svg_poses_x)
        y_max = max(svg_poses_y)
        scale = min(450 / abs(x_max-x_min), 450 / abs(y_max-y_min));
        half_height = abs(y_max-y_min) * scale/2
        half_width = abs(x_max-x_min) *scale /2

        first_pos = svg_poses.pop(0)
        answers["svg"] = "M " + str(mapValue(first_pos[0], x_min, x_max, -half_width, half_width)) + " " + str(mapValue(first_pos[1], y_min, y_max, -half_height, half_height)) + " " + " ".join(
            map(lambda pos: "L " + str(mapValue(pos[0], x_min, x_max, -half_width, half_width)) + " " + str(
                mapValue(pos[1], y_min, y_max, -half_height, half_height)), svg_poses))

        svg.write(Template("""<?xml version="1.0" encoding="utf-8"?>
    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
        viewBox="0 0 500 600"  >
    <style type="text/css">
    @font-face {
    font-family: 'Fredoka One';
    font-style: normal;
    font-weight: 400;
    font-display: swap;
    src: url(data:font/woff2;base64,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) format('woff2');
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }	.st0{fill:#E5C517;}
        .st2,.st3,.st0{font-family:'Fredoka One';}
        .st2{font-size:18px;}
        .st3{fill:#C72866;}
        .st4{font-size:28.8104px;}
        .st5{font-size:14px;}
        @keyframes dash {
  from {
    stroke-dashoffset: 1;
  }
  to {
    stroke-dashoffset: 0;
  }
}
#svg{
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: dash 3.5s linear forwards;}

    </style>

    <rect fill="none" x="10" y="110" width="480" height="480" rx="4" stroke="#E5C517" stroke-width="4" />
    <path pathLength="1" id="svg" fill="none" transform="translate(250 350) scale(1 -1)" d="$svg" stroke="#C72866" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
    <text xml:space="preserve" transform="matrix(1 0 0 1 17.292 68.3862)"><tspan class="st0 st2">Axiom: </tspan><tspan class="st3 st2">$axiom </tspan><tspan class="st0 st2">Angle: </tspan><tspan class="st3 st2">$angle° </tspan><tspan class="st0 st2">Evolution: </tspan><tspan class="st3 st2">$evolution</tspan></text>
    <g>
        <text transform="matrix(1 0 0 1 17.292 95.771)" class="st3 st2"><title>$rules</title>RULES</text>
    </g>
<g>
	<text transform="matrix(1 0 0 1 17.2922 38.4507)" class="st0 st1 st4">L-SYSTEMS</text>
	<a  href="https://github.com/GN-c/turtle-L-systems"><path class="st3" d="M480.6,19.9c-5.3,0-9.7,4.3-9.7,9.7c0,4.3,2.8,7.9,6.6,9.2c0.5,0.1,0.7-0.2,0.7-0.5c0-0.2,0-0.8,0-1.6
		c-2.7,0.6-3.3-1.3-3.3-1.3c-0.4-1.1-1.1-1.4-1.1-1.4c-0.9-0.6,0.1-0.6,0.1-0.6c1,0.1,1.5,1,1.5,1c0.9,1.5,2.3,1.1,2.8,0.8
		c0.1-0.6,0.3-1.1,0.6-1.3c-2.1-0.2-4.4-1.1-4.4-4.8c0-1.1,0.4-1.9,1-2.6c-0.1-0.2-0.4-1.2,0.1-2.6c0,0,0.8-0.3,2.7,1
		c0.8-0.2,1.6-0.3,2.4-0.3c0.8,0,1.6,0.1,2.4,0.3c1.8-1.3,2.7-1,2.7-1c0.5,1.3,0.2,2.3,0.1,2.6c0.6,0.7,1,1.5,1,2.6
		c0,3.7-2.3,4.5-4.4,4.8c0.3,0.3,0.7,0.9,0.7,1.8c0,1.3,0,2.3,0,2.7c0,0.3,0.2,0.6,0.7,0.5c3.8-1.3,6.6-4.9,6.6-9.2
		C490.3,24.3,485.9,19.9,480.6,19.9z"/></a>
</g>
    </svg>
    """).substitute(**answers))

turtle.Screen().exitonclick()
