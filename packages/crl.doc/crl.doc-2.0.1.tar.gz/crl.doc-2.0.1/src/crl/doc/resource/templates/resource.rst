{# Copyright (C) 2019, Nokia #}
{{ '=' * resourcefile.name|length }}
{{ resourcefile.name }}
{{ '=' * resourcefile.name|length }}

| **Resource Location:** {{ resourcefile.path }}
| **Attachment:**  :download:`Resource file <{{ resourcefile.name }}>`.

Settings and documentation
==========================

    .. robot-settings::
        :source: {{ resourcefile.path }}
        :style: expanded
{% if resourcefile.has_variables %}

Variables
=========

    .. robot-variables::
        :source: {{ resourcefile.path }}
        :style: expanded
{% endif %}
{% if resourcefile.has_keywords %}

Keywords
========

    .. robot-keywords::
       :source: {{ resourcefile.path }}
       :style: expanded
{% endif %}
{% if resourcefile.has_testcases %}

Testcases
=========

    .. robot-tests::
        :source: {{ resourcefile.path }}
        :style: expanded
{% endif %}
