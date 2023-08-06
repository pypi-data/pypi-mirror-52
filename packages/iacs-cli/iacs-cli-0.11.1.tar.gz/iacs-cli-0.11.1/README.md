# iacs-cli

### What is `iacs-cli`?

iacs-cli is a course website generator powered by
[Pelican](https://github.com/getpelican/pelican), a Python static site
generator, which will enable a course instructor to quickly convert course
content into a web content for students and the public. Some of the challenges
faced by IACS course instructor include:

1. Creating course materials often in Jupyter notebook, R markdown document, or
   Powerpoint slides. Unfortunately, course instructors are expected to upload
   these materials on to a website that must be maintained separately from course
   content. That means instructors must be versed in HTML, CSS, and sometimes
   JavaScript as well as website deployment. Ideally, course instructor should
   focus 100% of his or her effort in course content development and delegate
   website development to someone else.

2. Every IACS course instructor organizes the course project in his or her
   project organizational structure. This makes navigating course materials
   challenging for a new course instructor who takes over the curriculum.  
   Moreover, because of the lack of convention in how the course content is
   presented online, students also face difficulty of quickly finding materials
   on topic of their curiosity. Ideally, IACS course website should follow a
   consistent “look-and-feel,” and searching for learning contents should be
   intuitive and easy.

3. Course instructor should be able to quickly leverage existing content from
   the previous iteration of the course instead of starting the course project
   from scratch. Moreover, if course materials are organized following the same
   convention, it will be easier for course instructors to pull materials from
   other courses and integrate them into another course. For instance, if CS109
   Data Science must borrow concepts from AM207 Monte Carlo Methods, CS109
   instructor can copy the material - provided that CS109 course instructor has
   been proper credited - and present the material with small modifications and
   no concern for HTML and CSS.

`iacs-cli` alleviates these problems by enforcing course organization
conventions and automatic generation of static HTML and CSS files. In
addition to the static website generation, additional features of `iacs-cli`
include:

- Automatic topic index generation – course content can be organized around
  topics if a course designer provides “tags” information in the metadata of the content.

![Tag Indices](img/tag_indices.png)

- Search course content by topic – Like the topic index, if a course designer
  provides “tags” information, the website can be searched by topic of interest.

![Search Results](img/search_results.png)

- Customizable Web Design with minimal knowledge of HTML and CSS.  
  Without touching HTML or CSS, course designer can customize color of the
  website albeit maintaining consistent “feel” for IACS course.

![CS109A](img/cs109A.png)

![CS109B](img/cs109B.png)

![AM207](img/am207.png)

### Installation/Setup

`iacs-cli` is a PyPi package. In order to install through PyPi, use pip
command in the command console:

> \$ pip install iacs-cli

This command will install `iacs-cli` along with its dependencies:

- Click
- Pelican
- Markdown
- GitPython

### Workflow

1. Create a new project - Take the command console to the directory where you want to place your course content, and create the course using the following command:

> \$ iacs create 'course_name'

The standard convention we would like the instructors to use is YYYY-Course-Name.  
For example, for Fall 2017 CS109A, we would name the course project as 2017-CS109A.

2. Create the Home Page - The markdown document that converts to the home page
   of the website is pre-populated when you create the project directory. It is
   located in content/index.md

![index.md](img/index.png)

You must provide Title of the course and Date when the document was created.

**Do not modify save_as: index.html, unless you do not want to use this document as the home page of your course website**

3. Create other pages such as Syllabus, Policies, Resources, etc.

![syllabus.md](img/syllabus.png)

Every page that is not a course content such as the syllabus or resources page,
create markdown document (with the metadata of Title, Slug, and Date) inside
the directory `content/pages/`.

Here, Slug refers to the url to the webpage to be generated from the
document. For instance, Slug: syllabus will generate a url pointing to the
syllabus page: http://<course_website>/pages/syllabus.html

4. Create the Schedule page

`iacs-cli` enables course designers to create a table of course schedule using
csv file. In the publication process, the command line tool will automatically
convert the csv table into a markdown table, which in turn will be converted
to a HTML table.

When course designer creates a new project, schedule.csv file will be
automatically created inside `content/pages/` directory. Use Excel or similar
spreadsheet software to edit the schedule.csv file as shown below:

![schedule.csv](img/schedule.png)

Please note that any cell content that matches a title of markdown document,
then the created markdown will automatically link the markdown document to the
corresponding document. This auto-generated markdown table will then be
converted to HTML table with clickable links to the content of the course:

![schedule.html](img/schedule_page.png)

5. Edit Content of the course

There are two ways to create and edit contents of the course. One can create
a page using markdown or Ipython notebook.

Suggested directory structure:

```
ProjectDirectory
	content/
	labs/
lectures/
pages/
sections/
index.md
docs/
	plugins/
	ipynb/
	tipue_search/
	themes/
	static/
	templates/
	config.py
	README.md
```

6. Including Metadata
   In order to convert course content written in markdown or Ipython notebook,
   one must provide the following metadata information at the top of the document:

- Title
- Category
- Slug
- Author
- Date
- Tags – Optional, but highly encouraged for topic indexing and search

In markdown document, this may look like the example below:

![markdown](img/markdown.png)

For metadata for IPython Notebook, you must create a metadata file with the
same name but with a prefix of “-meta”. For example (see below),
for **lecture1213_notebook.ipynb**, create **lecture1213_notebook.ipynb-meta**
and provide metadata information at the top of the document.

![notebook](img/notebook.png)

7. Linking documents within a project

In order to create internal links between documents in a course, use markdown syntax for creating a link with {filename} prefix:

\(\< description \>\)\[\{ filename \}\< path_to_file \>\]

See example below:

![linking](img/linking.png)

8. Including static files such as \*.jpg, \*.pdf, and \*.png

For links to static files such as PDF or embedding JPEG or PNG images
in markdown document, use {attach} prefix:

\(\< description \>\)\[\{ attach \}\< path_to_file \>\]

9. After creating contents for the website, course designer must generate
   HTML and CSS documents using the following command inside the root directory
   of the project:

> \$ iacs publish

This command will populate the doc/ directory with static HTML and CSS files
for the website. To preview the website, use the following command inside
the root directory:

> \$ iacs launch

This command will launch a Python localhost server with port number 8000. Open
up a browser and visit http://localhost:8000/.

10. Turning on GitHub Pages

Commit and upload the git repo to Github.com. In settings page, enable GitHub
Pages and select **master branch /docs** folder as its source:

![Github Pages](img/github_pages.png)

### Command Reference

1. Create a new project

> \$ iacs create 'course_name'

2. Publish the content

> \$ iacs publish

3. Launch a localhost web server

> \$ iacs launch

4. Copy existing course projects

> \$ iacs copy 'existing_course_dir' 'course_name'
