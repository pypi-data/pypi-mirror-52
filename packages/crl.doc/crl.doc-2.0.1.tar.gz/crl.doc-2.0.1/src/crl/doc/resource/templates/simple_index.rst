{# Copyright (C) 2019, Nokia #}
{{ section }}
{{ "=" * section|length }}

{% for r in robotdocsconfs %}
{% for l in r.libraries %}
:doc:`{{ l.ref }}` - {{ l.synopsis }}
{% endfor %}
{% endfor %}
