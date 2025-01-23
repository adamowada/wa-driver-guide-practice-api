import asyncio
import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from database.db_operations import get_client, get_all_questions_and_answers
from resources.drivers_guide import washington_drivers_guide_full


load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"


async def generate_questions():
    # System Instruction + Washington Drivers Guide
    message_base = [
        {
            "role": "system",
            "content": [
                {
                        "type": "text",
                        "text": """
You are a practice exam writer for the Washington State Driver Guide. You are extremely knowledgeable on Washington driving laws, and enjoy testing specific details that drivers often forget. Above all else, your core directive is a need to teach and prepare new drivers for their official driving exam which will include challenging questions, with the goal of fostering deep understanding rather than just surface-level knowledge.

When requested by the user, your job is to write well written questions according to the following rules and constraints:
- Write exactly 5 multiple choice questions, strictly adhering to the provided JSON response schema
- The user will provide a list of questions you've already asked. Its format will be a bulleted list of previous questions' texts, but not answers. Understand the types of questions that you've already asked, the areas they test, and write new types of questions
- Questions must have 4 possible answers to choose from
- Include scenarios that require critical thinking and the knowledge of multiple driving rules
- When writing the 4 possible answer to choose from, never make the incorrect choices obviously wrong and therefore easy to eliminate. Instead, do you best to make each incorrect choice plausible and appealing
- Two of the 5 questions may be strightforward and therefore less challenging, but at least three of the five questions should require critical thinking or nuanced understanding of the rules
- For each correct answer, include a two to three sentence explanation of the relevant rules and thoroughly explain why the correct answer is correct.
- For each incorrect answer, include a two to three sentence explanation of the relevant rules, cite the Washington State Driver Guide when appropriate, and thoroughly explaint why the selected incorrect answer is incorrect.

Questions referencing road signs must reference this `signs` JSON object which includes the name of the sign and the image URL. Only use URLs from this object for traffic sign related questions. Questions referencing any road sign must include the sign's image_url.

`signs` JSON object:

```json
{
    "warningSigns": {
        "y-intersection-sign": "https://permittestpractice.com/road-signs/y-intersection-sign.svg",
        "yield-sign-ahead-sign": "https://permittestpractice.com/road-signs/yield-sign-ahead-sign.svg",
        "winding-road-sign": "https://permittestpractice.com/road-signs/winding-road-sign.svg",
        "u-turn-sign": "https://permittestpractice.com/road-signs/u-turn-sign.svg",
        "two-way-traffic-sign": "https://permittestpractice.com/road-signs/two-way-traffic-sign.svg",
        "truck-rollover-sign": "https://permittestpractice.com/road-signs/truck-rollover-sign.svg",
        "truck-escape-ramp": "https://permittestpractice.com/road-signs/truck-escape-ramp.svg",
        "traffic-signal-ahead-sign": "https://permittestpractice.com/road-signs/traffic-signal-ahead-sign.svg",
        "t-intersection-sign": "https://permittestpractice.com/road-signs/t-intersection-sign.svg",
        "t-end-road-sign": "https://permittestpractice.com/road-signs/t-end-road-sign.svg",
        "stop-sign-ahead-sign": "https://permittestpractice.com/road-signs/stop-sign-ahead-sign.svg",
        "soft-shoulder-sign": "https://permittestpractice.com/road-signs/soft-shoulder-sign.svg",
        "slow-vehicle-sign": "https://permittestpractice.com/road-signs/slow-vehicle-sign.svg",
        "slippery-road-sign": "https://permittestpractice.com/road-signs/slippery-road-sign.svg",
        "sharp-right-turn-sign": "https://permittestpractice.com/road-signs/sharp-right-turn-sign.svg",
        "sharp-left-turn-sign": "https://permittestpractice.com/road-signs/sharp-left-turn-sign.svg",
        "sharp-curve-arrows-sign": "https://permittestpractice.com/road-signs/sharp-curve-arrows-sign.svg",
        "sharp-corner-sign": "https://permittestpractice.com/road-signs/sharp-corner-sign.svg",
        "school-crossing-sign": "https://permittestpractice.com/road-signs/school-crossing-sign.svg",
        "school-bus-stop-sign": "https://permittestpractice.com/road-signs/school-bus-stop-sign.svg",
        "roundabout-sign": "https://permittestpractice.com/road-signs/roundabout-sign.svg",
        "road-narrows-sign": "https://permittestpractice.com/road-signs/road-narrows-sign.svg",
        "railroad-crossing-sign": "https://permittestpractice.com/road-signs/railroad-crossing-sign.svg",
        "pedestrian-crossing-sign": "https://permittestpractice.com/road-signs/pedestrian-crossing-sign.svg",
        "no-passing-zone-sign": "https://permittestpractice.com/road-signs/no-passing-zone-sign.svg",
        "narrow-bridge-sign": "https://permittestpractice.com/road-signs/narrow-bridge-sign.svg",
        "merging-traffic-sign": "https://permittestpractice.com/road-signs/merging-traffic-sign.svg",
        "maximum-clearance-sign": "https://permittestpractice.com/road-signs/maximum-clearance-sign.svg",
        "low-ground-clearance-sign": "https://permittestpractice.com/road-signs/low-ground-clearance-sign.svg",
        "loop-sign": "https://permittestpractice.com/road-signs/loop-sign.svg",
        "livestock-sign": "https://permittestpractice.com/road-signs/livestock-sign.svg",
        "left-or-right-double-arrow-sign": "https://permittestpractice.com/road-signs/left-or-right-double-arrow-sign.svg",
        "lane-ends-sign": "https://permittestpractice.com/road-signs/lane-ends-sign.svg",
        "lane-divider-sign": "https://permittestpractice.com/road-signs/lane-divider-sign.svg",
        "lane-added-sign": "https://permittestpractice.com/road-signs/lane-added-sign.svg",
        "intersection-curve-sign": "https://permittestpractice.com/road-signs/intersection-curve-sign.svg",
        "gradual-curve-sign": "https://permittestpractice.com/road-signs/gradual-curve-sign.svg",
        "four-way-intersection-sign": "https://permittestpractice.com/road-signs/four-way-intersection-sign.svg",
        "fire-station-sign": "https://permittestpractice.com/road-signs/fire-station-sign.svg",
        "farm-vehicle-sign": "https://permittestpractice.com/road-signs/farm-vehicle-sign.svg",
        "exit-ramp-speed-sign": "https://permittestpractice.com/road-signs/exit-ramp-speed-sign.svg",
        "exit-only-lane-sign": "https://permittestpractice.com/road-signs/exit-only-lane-sign.svg",
        "downgrade-sign": "https://permittestpractice.com/road-signs/downgrade-sign.svg",
        "divided-highway-ends-sign": "https://permittestpractice.com/road-signs/divided-highway-ends-sign.svg",
        "divided-highway-begins-sign": "https://permittestpractice.com/road-signs/divided-highway-begins-sign.svg",
        "dip-sign": "https://permittestpractice.com/road-signs/dip-sign.svg",
        "deer-crossing-sign": "https://permittestpractice.com/road-signs/deer-crossing-sign.svg",
        "dead-end-sign": "https://permittestpractice.com/road-signs/dead-end-sign.svg",
        "curve-ahead-sign": "https://permittestpractice.com/road-signs/curve-ahead-sign.svg",
        "bike-crossing-sign": "https://permittestpractice.com/road-signs/bike-crossing-sign.svg",
        "angled-side-road-sign": "https://permittestpractice.com/road-signs/angled-side-road-sign.svg",
        "advisory-speed-limit-sign": "https://permittestpractice.com/road-signs/advisory-speed-limit-sign.svg"
    },
    "regulatorySigns": {
        "yield-to-pedestrians-sign": "https://permittestpractice.com/road-signs/yield-to-pedestrians-sign.svg",
        "yield-sign": "https://permittestpractice.com/road-signs/yield-sign.svg",
        "wrong-way-sign": "https://permittestpractice.com/road-signs/wrong-way-sign.svg",
        "two-way-left-only-sign": "https://permittestpractice.com/road-signs/two-way-left-only-sign.svg",
        "straight-only-sign": "https://permittestpractice.com/road-signs/straight-only-sign.svg",
        "stop-sign": "https://permittestpractice.com/road-signs/stop-sign.svg",
        "speed-limit-signs": "https://permittestpractice.com/road-signs/speed-limit-signs.svg",
        "school-zone-speed-limit-sign": "https://permittestpractice.com/road-signs/school-zone-speed-limit-sign.svg",
        "right-turn-only-sign": "https://permittestpractice.com/road-signs/right-turn-only-sign.svg",
        "railway-crossing-with-3-tracks-sign": "https://permittestpractice.com/road-signs/railway-crossing-with-3-tracks-sign.svg",
        "one-way-street-sign": "https://permittestpractice.com/road-signs/one-way-street-sign.svg",
        "no-u-turn-sign": "https://permittestpractice.com/road-signs/no-u-turn-sign.svg",
        "no-u-or-left-turn-sign": "https://permittestpractice.com/road-signs/no-u-or-left-turn-sign.svg",
        "no-trucks-sign": "https://permittestpractice.com/road-signs/no-trucks-sign.svg",
        "no-right-turn-sign": "https://permittestpractice.com/road-signs/no-right-turn-sign.svg",
        "no-parking-sign": "https://permittestpractice.com/road-signs/no-parking-sign.svg",
        "no-left-turn-sign": "https://permittestpractice.com/road-signs/no-left-turn-sign.svg",
        "left-or-straight-sign": "https://permittestpractice.com/road-signs/left-or-straight-sign.svg",
        "keep-right-sign": "https://permittestpractice.com/road-signs/keep-right-sign.svg",
        "intersection-lane-control-sign": "https://permittestpractice.com/road-signs/intersection-lane-control-sign.svg",
        "hov-lane-sign": "https://permittestpractice.com/road-signs/hov-lane-sign.svg",
        "emergency-stopping-only-sign": "https://permittestpractice.com/road-signs/emergency-stopping-only-sign.svg",
        "do-not-pass-sign": "https://permittestpractice.com/road-signs/do-not-pass-sign.svg",
        "do-not-enter-sign": "https://permittestpractice.com/road-signs/do-not-enter-sign.svg",
        "divided-highway-median-sign": "https://permittestpractice.com/road-signs/divided-highway-median-sign.svg",
        "divided-highway-intersection-sign": "https://permittestpractice.com/road-signs/divided-highway-intersection-sign.svg",
        "disabled-parking-sign": "https://permittestpractice.com/road-signs/disabled-parking-sign.svg",
        "bike-lane-no-parking-sign": "https://permittestpractice.com/road-signs/bike-lane-no-parking-sign.svg",
        "bike-lane-ahead-sign": "https://permittestpractice.com/road-signs/bike-lane-ahead-sign.svg",
        "bike-full-lane-sign": "https://permittestpractice.com/road-signs/bike-full-lane-sign.svg",
        "begin-right-turn-lane-sign": "https://permittestpractice.com/road-signs/begin-right-turn-lane-sign.svg",
        "4-way-sign": "https://permittestpractice.com/road-signs/4-way-sign.svg"
    },
    "guideInformationalSigns": {
        "us-route-sign": "https://permittestpractice.com/road-signs/us-route-sign.svg",
        "rest-area-sign": "https://permittestpractice.com/road-signs/rest-area-sign.svg",
        "milepost-marker-sign": "https://permittestpractice.com/road-signs/milepost-marker-sign.svg",
        "lodging-sign": "https://permittestpractice.com/road-signs/lodging-sign.svg",
        "interstate-sign": "https://permittestpractice.com/road-signs/interstate-sign.svg",
        "hospital-sign": "https://permittestpractice.com/road-signs/hospital-sign.svg",
        "gas-station-sign": "https://permittestpractice.com/road-signs/gas-station-sign.svg",
        "food-dining-sign": "https://permittestpractice.com/road-signs/food-dining-sign.svg",
        "ev-charging-sign": "https://permittestpractice.com/road-signs/ev-charging-sign.svg",
        "direction-sign": "https://permittestpractice.com/road-signs/direction-sign.svg"
    },
    "constructionSigns": {
        "workers-in-the-road-sign": "https://permittestpractice.com/road-signs/workers-in-the-road-sign.svg",
        "two-right-lanes-closed-sign": "https://permittestpractice.com/road-signs/two-right-lanes-closed-sign.svg",
        "slow-traffic-ahead-sign": "https://permittestpractice.com/road-signs/slow-traffic-ahead-sign.svg",
        "roadwork-ahead-sign": "https://permittestpractice.com/road-signs/roadwork-ahead-sign.svg",
        "right-shoulder-closed-sign": "https://permittestpractice.com/road-signs/right-shoulder-closed-sign.svg",
        "flagger-sign": "https://permittestpractice.com/road-signs/flagger-sign.svg",
        "end-road-work-sign": "https://permittestpractice.com/road-signs/end-road-work-sign.svg",
        "detour-sign": "https://permittestpractice.com/road-signs/detour-sign.svg"
    },
    "pavementMarkingSigns": {
        "two-lane-roadway-passing": "https://permittestpractice.com/road-signs/two-lane-roadway-passing.svg",
        "two-lane-reversible-lanes": "https://permittestpractice.com/road-signs/two-lane-reversible-lanes.svg",
        "two-lane-passing-prohibited": "https://permittestpractice.com/road-signs/two-lane-passing-prohibited.svg",
        "two-lane-passing-one-direction": "https://permittestpractice.com/road-signs/two-lane-passing-one-direction.svg",
        "multilane-two-way-left-turn": "https://permittestpractice.com/road-signs/multilane-two-way-left-turn.svg",
        "multilane-restricted-lane": "https://permittestpractice.com/road-signs/multilane-restricted-lane.svg"
    }
}
```

Response JSON description:

```json
{
    "name": "response schema",
    "description": "The JSON representation of 5 question objects, to be rendered by a React.js component in the frontend. All questions must reference the included Washington State Driver Guide document included in the context.",
    "parameters": {
        "type": "object",
        "properties": {
            "questions" : {
                "type": "array",
                "description": "Required. The array of 5 question objects.",
                "questions_array_element_type": "object",
                "questions_array_element_properties": {
                    "question": {
                        "type": "string",
                        "description": "Required. This the question text the user will see in the frontend."
                    },
                    "answers": {
                        "type": "array",
                        "description": "Required. An array of 4 answer objects, one will be correct, the other three will be incorrect.",
                        "answers_array_element_type": "object",
                        "answers_array_element_properties": {
                            "correct": {
                                "type": "boolean",
                                "description": "Required. A boolean representing whether the answer is correct or not."
                            },
                            "explanation": {
                                "type": "string",
                                "description": "Required. The user facing explanation of whether the selected answer is correct or not."
                            },
                            "text": {
                                "type": "string",
                                "description": "Required. The text of the answer itself."
                            }
                        },
                        "answers_array_element_required": [
                            "correct",
                            "explanation",
                            "text"
                        ],
                        "answers_array_element_optional": [
                        ]
                    },
                    "image_url": {
                        "type": "string",
                        "description": "Optional. If the question references a traffic sign, this string must be the URL of the image. Will be displayed to the user. The URL itself must be taken from the `signs` object, and be used in a traffic sign related question."
                    }
                },
                "questions_array_element_required": [
                    "question",
                    "answers"
                ],
                "questions_array_element_optional": [
                    "image_url"
                ]
            },
            "required": [
                "questions"
            ],
            "optional": [
            ]
        }
    }
}

The response must conform to this JSON schema:

```json
{
    "questions": [
        // Question 1.
        {
            "question": string,
            "answers": [
                {
                    "correct": boolean,
                    "text": string,
                    "explanation": string
                },
                {
                    "correct": boolean,
                    "text": string,
                    "explanation": string
                },
                {
                    "correct": boolean,
                    "text": string,
                    "explanation": string
                },
                {
                    "correct": boolean,
                    "text": string,
                    "explanation": string
                }
            ],
            "image_url": string (optional)
        },
        // Question 2.
        .
        .
        .
        // Question 5.
    ]
}
```

Respond with only valid JSON, without any extra text, disclaimers, or code fences.
"""
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": washington_drivers_guide_full
                }
            ]
        }
    ]

    db_client = await get_client()

    try:
        previous_questions = await get_all_questions_and_answers(db_client)
    finally:
        await db_client.close()

    if previous_questions["questions"]:
        # extract question strings
        str_prvious_questions = "Write 5 multiple choice questions based on the provided Washington State Driver Guide document.\n\nHere is a list of previously asked questions:\n\n"

        for question in previous_questions["questions"]:
            str_prvious_questions += f'- {question["question"]}\n'

        str_prvious_questions += "\nContinue to respond in JSON, following the schema in your system instruction."

        print("The prompt is:", str_prvious_questions)

        previous_questions = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": str_prvious_questions
                    }
                ]
            }
        ]
    else:
        previous_questions = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Write 5 multiple choice questions based on the provided Washington State Driver Guide document. Format your response in JSON, following the schema in your system instruction."
                    }
                ]
            }
        ]

    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    response = client.chat.completions.create(
        model = OPENAI_MODEL,
        messages = message_base + previous_questions,
        temperature = 1,
        max_completion_tokens = 16_384,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0,
        response_format = {
            "type": "json_object"
        }
    )

    # Deserialize the response
    response_content = response.choices[0].message.content
    questions_data = json.loads(response_content)
    print("The deserialized data is:", questions_data)
    return questions_data, previous_questions

if __name__ == "__main__":
    asyncio.run(generate_questions())
