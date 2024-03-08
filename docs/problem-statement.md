# Key-Value Server

Your job is to build a simple [key-value server](https://en.wikipedia.org/wiki/Key%E2%80%93value_database) for immutable data on [FASTAPI Framework](https://fastapi.tiangolo.com/).

To make the task easier, the server only serves read-only data that is provided in a separate file. The data doesn't need to be mutated in any way by the server. Clients need to be able to contact the server over network (you can choose the protocol), send a query containing a key, and the server will answer with the corresponding value from the dataset, if the given key exists.

The key-value data is provided in the following format:
```
3479d894-3271-4935-88cf-a06f3cbb80a5 this is a value
f8a24bb8-eff8-41dc-929b-10b4c3e49e05 1234
0cdfafb5-edb4-48a6-a7ec-5b1a75831f91 here is another value
```
The first column contains the key which is always a valid [UUID (version 4)](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random)). A single space character separates the key from the value that is the rest of the line until a newline (\n) character. You can use an example data file stored in this repository, `example.data`, for testing.

In addition to implementing the server, provide an example how a client can request data from the server. The client will provide only a key, e.g. `f8a24bb8-eff8-41dc-929b-10b4c3e49e05`, and the server needs to provide the corresponding value in the response, in this case, `1234`.

Your implementation should be able to handle files that contain up to a million key-value pairs.

**Important**: You should be able to explain how your system works in detail and answer follow up questions like these:

- How much data can your server handle? How could you improve it so it can handle even larger datasets?
- How many milliseconds it takes for the client to get a response on average? How could you improve the latency?
- What are some failure patterns that you can anticipate?

While external python libraries are allowed, You are not allowed to use any external infrastructure or db for processing.

Please don't spend more than 1-2 hours solving this problem. If you have ideas about how to improve your solution if more time was available, save them for the follow-up discussion about possible improvements and their relative pros and cons. For this reason, the question is deliberately open-ended - there is not a single right answer or any tricks or gotchas.

Deliverables:
Github repo with documentation, proper structuring of API, and pytests with production level standards. You will be tested on the structural representation of code and how you handle the data.

Submission Guidelines
Email your github link to interviewer email with the subject "[IONET] [PYTHON ASSIGNMENT] [NAME]"
