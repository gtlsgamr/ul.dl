 ul.dl, a no-bullshit file hosting service.    
----------------------------------------------------

HTTP POST files here:
    curl -F'file=@yourfile.png' yourdomain

Maximum file size: 20.0 MiB

TERMS OF SERVICE
----------------

ul.dl is NOT a platform for:
* piracy
* pornography and gore
* extremist material of any kind
* malware / botnet C&C
* anything related to crypto currencies
* backups
* CI build artifacts
* doxxing, database dumps containing personal information

Uploads found to be in violation of these rules will be removed,
and the originating IP address blocked from further uploads.

REQUIREMENTS
---------------
You need to have [nodejs](https://nodejs.org/en/) and [npm](https://www.npmjs.com/) installed.

INSTALLATION
---------------

You can deploy it like any other node project.

1. Clone the repository

    `git clone https://github.com/gtlsgamr/ul.dl`

2. Install the dependencies 

    `npm i`

3. Set your configurations in app.js (e.g. port to run on, your url, etc)

4. `npm start`

Big props to 0x0.st for inspiring this, this project is much less featured than it but again, that was the objective.
