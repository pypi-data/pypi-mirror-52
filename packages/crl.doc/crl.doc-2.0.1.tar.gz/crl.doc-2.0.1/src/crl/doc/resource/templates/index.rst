{# Copyright (C) 2019, Nokia #}
{{ section }}
{{ "=" * section|length }}

{% for r in robotdocsconfs %}
{{ r.name }}
{{ "-" * r.name|length }}

{{ r.description }}

{% for l in r.libraries %}
:doc:`{{ l.ref }}` - {{ l.synopsis }}
{% endfor %}
{% endfor %}
