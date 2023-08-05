# girepo 
<a id="markdown-girepo" name="girepo"></a>
[![pypi version](https://img.shields.io/pypi/v/girepo.svg?style=flat)](https://pypi.org/project/girepo/)
[![CircleCI Status](https://circleci.com/gh/ta08/girepo.svg?style=shield)](https://circleci.com/gh/ta08/girepo)

This makes it easy to investigate repositories at Github and to describe the results as a markdown table format. 

<!-- TOC -->

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
    - [Simple (ver. rough)](#simple-ver-rough)
    - [Simple (ver. strict)](#simple-ver-strict)
    - [Input From File](#input-from-file)
    - [Whitespace](#whitespace)
    - [etc](#etc)

<!-- /TOC -->

## Installation
<a id="markdown-installation" name="installation"></a>

```
pip install girepo
```

## Usage
<a id="markdown-usage" name="usage"></a>

```markdown
usage: girepo [-h] {rough,ro,strict,st} ...

Print Git Repositories information with the markdown format for your
documents. This uses github api without authentication. So you could reach the
rate-limitation if you use this 60 requests per hour.
https://developer.github.com/v3/#rate-limiting Could you take a cup of coffee
☕ until recovering if you exceed.

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  you can choose a search way from sub commands. rough sub command does not
  require owner info but it might return wrong info.

  {rough,ro,strict,st}
    rough (ro)          heuristic search. see `girepo ro --help`
    strict (st)         strict search. see `girepo st --help`

God bless you.


```
## Example
<a id="markdown-example" name="example"></a>

### Simple (ver. rough)
<a id="markdown-simple-ver-rough" name="simple-ver-rough"></a>

If you want to investigate repositories of frontend framework, you can run this script like below.

```sh
girepo rough angular react vue
```

Output:
```markdown
| fullname | star | star/day | created_at | updated_at | license | language | description | url |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| angular/angular | 51,080 | 28.17 | 2014-09-18 | 2019-09-05 | MIT License | TypeScript | One framework. Mobile & desktop. | [link](https://github.com/angular/angular) |
| facebook/react | 135,563 | 59.07 | 2013-05-24 | 2019-09-05 | MIT License | JavaScript | A declarative, efficient, and flexible JavaScript library for building user interfaces. | [link](https://github.com/facebook/react) |
| vuejs/vue | 147,494 | 66.14 | 2013-07-29 | 2019-09-05 | MIT License | JavaScript | 🖖 Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web. | [link](https://github.com/vuejs/vue) |
```

Then you can get the table format of markdown.

| fullname | star | star/day | created_at | updated_at | license | language | description | url |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| angular/angular | 51,080 | 28.17 | 2014-09-18 | 2019-09-05 | MIT License | TypeScript | One framework. Mobile & desktop. | [link](https://github.com/angular/angular) |
| facebook/react | 135,563 | 59.07 | 2013-05-24 | 2019-09-05 | MIT License | JavaScript | A declarative, efficient, and flexible JavaScript library for building user interfaces. | [link](https://github.com/facebook/react) |
| vuejs/vue | 147,494 | 66.14 | 2013-07-29 | 2019-09-05 | MIT License | JavaScript | 🖖 Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web. | [link](https://github.com/vuejs/vue) |


This results are heuristic so if you find wrong rows,
 I recommend to use strict sub-command with the fullname and the headless option. 


### Simple (ver. strict)
<a id="markdown-simple-ver-strict" name="simple-ver-strict"></a>

If you want to investigate repositories of frontend framework, you can run this script like below.

```sh
girepo strict angular/angular facebook/react vuejs/vue 
```

Output:
```markdown
| fullname | star | star/day | created_at | updated_at | license | language | description | url |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| angular/angular | 51,080 | 28.17 | 2014-09-18 | 2019-09-05 | MIT License | TypeScript | One framework. Mobile & desktop. | [link](https://github.com/angular/angular) |
| facebook/react | 135,563 | 59.07 | 2013-05-24 | 2019-09-05 | MIT License | JavaScript | A declarative, efficient, and flexible JavaScript library for building user interfaces. | [link](https://github.com/facebook/react) |
| vuejs/vue | 147,494 | 66.14 | 2013-07-29 | 2019-09-05 | MIT License | JavaScript | 🖖 Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web. | [link](https://github.com/vuejs/vue) |
```

Then you can get the table format of markdown.

| fullname | star | star/day | created_at | updated_at | license | language | description | url |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| angular/angular | 51,080 | 28.17 | 2014-09-18 | 2019-09-05 | MIT License | TypeScript | One framework. Mobile & desktop. | [link](https://github.com/angular/angular) |
| facebook/react | 135,563 | 59.07 | 2013-05-24 | 2019-09-05 | MIT License | JavaScript | A declarative, efficient, and flexible JavaScript library for building user interfaces. | [link](https://github.com/facebook/react) |
| vuejs/vue | 147,494 | 66.14 | 2013-07-29 | 2019-09-05 | MIT License | JavaScript | 🖖 Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web. | [link](https://github.com/vuejs/vue) |



### Input From File
<a id="markdown-input-from-file" name="input-from-file"></a>

If you want to use a bulk input, please prepare a file whose content is like below. Do not contain a blank line.

```markdown
angular/angular
facebook/react
vuetifyjs / vuetify
vuejs/vue
```

For example, if the file name is ./misc/input.txt, then

```sh
girepo strict @misc/input.txt
```

Output:
```markdown
| fullname | star | star/day | created_at | updated_at | license | language | description | url |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| angular/angular | 51,080 | 28.17 | 2014-09-18 | 2019-09-05 | MIT License | TypeScript | One framework. Mobile & desktop. | [link](https://github.com/angular/angular) |
| facebook/react | 135,563 | 59.07 | 2013-05-24 | 2019-09-05 | MIT License | JavaScript | A declarative, efficient, and flexible JavaScript library for building user interfaces. | [link](https://github.com/facebook/react) |
| vuetifyjs/vuetify | 21,394 | 19.65 | 2016-09-12 | 2019-09-05 | MIT License | TypeScript | 🐉 Material Component Framework for Vue.js 2 | [link](https://github.com/vuetifyjs/vuetify) |
| vuejs/vue | 147,494 | 66.14 | 2013-07-29 | 2019-09-05 | MIT License | JavaScript | 🖖 Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web. | [link](https://github.com/vuejs/vue) |
```


### Whitespace
<a id="markdown-whitespace" name="simple-whitespace"></a>

when you copy a name of an owner and a repository on a topic page the below, you might get whitespaces between the owner and repository like ` vuetifyjs / vuetify `. So this script enables to parse them. 

![topic_page](misc/screenshot.png)

Please surround the owner/repository name with " if it contains whitespaces. 

```sh
girepo strict " vuetifyjs / vuetify " "kriasoft / react-starter-kit " 
```

Output:

```markdown
| fullname | star | star/day | created_at | updated_at | license | language | description | url |
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
| vuetifyjs/vuetify | 21,394 | 19.65 | 2016-09-12 | 2019-09-05 | MIT License | TypeScript | 🐉 Material Component Framework for Vue.js 2 | [link](https://github.com/vuetifyjs/vuetify) |
| kriasoft/react-starter-kit | 19,484 | 9.9 | 2014-04-16 | 2019-09-05 | MIT License | JavaScript | React Starter Kit — isomorphic web app boilerplate (Node.js, Express, GraphQL, React.js, Babel, PostCSS, Webpack, Browsersync) | [link](https://github.com/kriasoft/react-starter-kit) |
```

### etc
<a id="markdown-etc" name="etc"></a>

```sh
girepo strict angular/angular facebook/react vuejs/vue  --asc star
```

```sh
girepo rough angular react vue  --headless
```


