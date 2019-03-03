# -*- coding: utf-8 -*-

import re


class JiraMarkdown:
    @staticmethod
    def jira_to_html(jira_text = None):
        text = jira_text
        #Headers
        text = re.sub(r'(?:\nh|^h)([1-6])\. (.*)\n', r'<h\1>\2</h\1>', text)
        #Strong
        text = re.sub(r'\*(.*)\*', r'<b>\1</b>', text)
        #Emphasis
        text = re.sub(r'_(.*)_', r'<em>\1</em>', text)
        #Citation
        text = re.sub(r'\?\?(.*)\?\?', r'<cite>\1</cite>', text)
        #Deleted
        text = re.sub(r'-(.*)-', r'<s>\1</s>', text)
        #Inserted
        text = re.sub(r'\+(.*)\+', r'<u>\1</u>', text)
        #Superscript
        text = re.sub(r'\^(.*)\^', r'<sup>\1</sup>', text)
        #Subscript
        text = re.sub(r'\*(.*)\*', r'<sub>\1</sub>', text)
        #Monospaced
        #Blockquote
        text = re.sub(r'(?:^bq. |\nbq. )(.*)', r'<blockquote>\1</blockquote>', text)
        text = re.sub(r'\{quote\}((?:.|\n)*)\{quote\}\n', r'<blockquote>\1</blockquote>', text)
        #Horizontal rule
        text = re.sub(r'----\n', r'<hr />', text)
        #Text color
        #Code
        #Lists
        #Line breaks

        return text
