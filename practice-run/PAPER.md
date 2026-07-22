# ICT2216 Secure Software Development — Practical Test (Practice Paper)

Adapted from the AY2022/2023 Trimester 1 paper, with **Jenkins replaced by GitHub Actions**.

This test paper comprises **TWO (2) Sections** with **EIGHT (8) Questions** in total.

- Answer all questions.
- For the submission, submit a zip file as **`StudentID.zip`**.
- **Make sure everything can be executed by the command `docker-compose up`** after the
  marker unzips the file.
- Reserve enough time to submit your file, as the folder can be larger than 300 MB.
- Logout and restart the lab PC once you have completed the practical test.

---

## Section 1

**Q1.** Download the `Question.zip` file from LMS. The password of the zip file will be
provided in the lab session.

> *Practice substitute:* use the provided `Question/` folder in this directory as your
> starting point. Copy it somewhere else first (see `README.md`).

**Q2.** Execute `docker-compose up` and verify the web server is up and running.
The nginx webserver can be accessed via:

    http://127.0.0.1/

**Q3.** Set up Git in the Docker Compose. Configure the Git account identity as follows:

    Username for the git: "Your-full-name"
    Email for the git:    "Your-sit-email"

**Q4.** Write a simple web application in a language of your choice. You can use another
web application container to replace nginx. The web application should meet the
following requirements:

*(Attempt **ONE** of the two versions below — pick one at random to simulate not knowing
which you'll get.)*

### Version 1 — Input validation

- (a) A default home page with a form containing one input field for the user to enter a
  search term and a submit button.
- (b) A function/method to verify the search term to prevent XSS attack, based on
  **OWASP Top 10 Proactive Control C5: Validate All Inputs**, and other relevant references.
- (c) If the input is validated to be an XSS attack, clear the input and remain on the
  home page for new input.
- (d) If the input is validated to be a SQL injection attack, clear the input and remain
  on the home page for new input.
- (e) If the input is not an XSS attack, go to a new page to display the search term, and
  a button to return to the home page.
- (f) If the input is not a SQL injection attack, go to a new page to display the search
  term, and a button to return to the home page.
- (g) No mark is awarded for UI since this is a module on SSD and not HCI.
- (h) Marks will be deducted for code which is unnecessarily long and complex.
- (i) Commit your code to the Git set up in Q3.

### Version 2 — Password requirements

- (a) A default home page with a form containing one input field for the entering of a
  password and a login button.
- (b) A function/method to verify the password based on **OWASP Top 10 Proactive Controls
  C6: Implement Digital Identity** under **Level 1: Passwords – Password Requirements**.
- (c) No requirement for MFA.
- (d) Block the common passwords that are leaked as compiled in the file
  `10-million-password-list-top-1000.txt` at
  https://github.com/danielmiessler/SecLists/tree/master/Passwords/Common-Credentials
- (e) If the password does not meet the requirements, remain at the home page.
- (f) If the password passes the requirements, go to a Welcome page displaying the
  password and a logout button for returning to the home page.
- (g) No mark is awarded for UI since this is a module on SSD and not HCI.
- (h) Marks will be deducted for code which is unnecessarily long and complex.
- (i) Commit your code to the Git set up in Q3.

**Q5.** Create a **GitHub Actions workflow** in your Git repository to perform
**integration**, **dependency check** and **UI testing over HTTP** on your web
application written in Q4.

---

## Section 2

**Q6.** Set up **SonarQube** in the docker-compose. Configure the username as `admin` and
the password to be your student ID. SonarQube should be configured to be accessed via:

    http://127.0.0.1:9000/

**Q7.** Integrate SonarQube scanning into the pipeline you created in Section 1 Q5.
SonarQube should show the scanning result of your source code.

**Q8.** If there are any bugs, vulnerabilities and security hotspots, please fix the code
and do the scanning again. The result should show that all the bugs, vulnerabilities and
security hotspots are fixed.

> **Note/tip:** You may face a memory issue when running SonarQube.

--- End of paper ---
