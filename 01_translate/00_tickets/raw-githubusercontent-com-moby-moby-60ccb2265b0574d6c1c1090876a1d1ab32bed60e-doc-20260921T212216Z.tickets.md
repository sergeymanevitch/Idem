snapshot: raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt
sha256: d5cfeba8e2effb279f33fac41e317078f4460f921d9ef7379927d2ab5dd792b6
source_url: https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md
body_range: 1-250
line_numbers: snapshot

## Ticket 1

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/upgrade` upgrade a plugin. | 20 | * `POST /plugins/(plugin name)/upgrade` upgrade a plugin. |
| affected_surface | `POST /plugins/(plugin name)/upgrade` | 20 | * `POST /plugins/(plugin name)/upgrade` upgrade a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 20 |  |

## Ticket 2

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. | 26 | * The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. |
| affected_surface | `/containers/json` | 26 | * The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. |
| affected_surface | `/v1.25/containers/json` | 26 | * The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. | 26 | * The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 26 |  |

## Ticket 3

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /version` now returns `MinAPIVersion`. | 27 | * `GET /version` now returns `MinAPIVersion`. |
| affected_surface | `GET /version` | 27 | * `GET /version` now returns `MinAPIVersion`. |
| affected_surface | `MinAPIVersion` | 27 | * `GET /version` now returns `MinAPIVersion`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 27 |  |

## Ticket 4

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` accepts `networkmode` parameter to specify network used during build. | 28 | * `POST /build` accepts `networkmode` parameter to specify network used during build. |
| affected_surface | `POST /build` | 28 | * `POST /build` accepts `networkmode` parameter to specify network used during build. |
| affected_surface | `networkmode` | 28 | * `POST /build` accepts `networkmode` parameter to specify network used during build. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 28 |  |

## Ticket 5

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/(name)/json` now returns `OsVersion` if populated | 29 | * `GET /images/(name)/json` now returns `OsVersion` if populated |
| affected_surface | `GET /images/(name)/json` | 29 | * `GET /images/(name)/json` now returns `OsVersion` if populated |
| affected_surface | `OsVersion` | 29 | * `GET /images/(name)/json` now returns `OsVersion` if populated |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 29 |  |

## Ticket 6

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `Isolation`. | 30 | * `GET /info` now returns `Isolation`. |
| affected_surface | `GET /info` | 30 | * `GET /info` now returns `Isolation`. |
| affected_surface | `Isolation` | 30 | * `GET /info` now returns `Isolation`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 30 |  |

## Ticket 7

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits. | 31 | * `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits. |
| affected_surface | `POST /containers/create` | 31 | * `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits. |
| affected_surface | `AutoRemove` | 31 | * `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 31 |  |

## Ticket 8

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| affected_surface | `GET /containers/json` | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| affected_surface | `GET /containers/(id or name)/json` | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| affected_surface | `"removing"` | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| affected_surface | `State.Status` | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 32 |  |

## Ticket 9

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. | 33 | * `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. |
| affected_surface | `GET /containers/json` | 33 | * `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. |
| affected_surface | `removing` | 33 | * `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. |
| affected_surface | `status` | 33 | * `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 33 |  |

## Ticket 10

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now supports filtering containers by `health` status. | 34 | * `GET /containers/json` now supports filtering containers by `health` status. |
| affected_surface | `GET /containers/json` | 34 | * `GET /containers/json` now supports filtering containers by `health` status. |
| affected_surface | `health` | 34 | * `GET /containers/json` now supports filtering containers by `health` status. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 34 |  |

## Ticket 11

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. | 35 | * `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. |
| affected_surface | `DELETE /volumes/(name)` | 35 | * `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. |
| affected_surface | `force` | 35 | * `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. |
| affected_surface | query | 35 | * `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 35 |  |

## Ticket 12

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies. | 36 | * `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies. |
| affected_surface | `POST /containers/create/` | 36 | * `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies. |
| affected_surface | `POST /containers/(name)/update` | 36 | * `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 36 |  |

## Ticket 13

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| affected_surface | `POST /containers/create` | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| affected_surface | `--ip` | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| affected_surface | `--ip6` | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| affected_surface | `docker create/run` | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 37 |  |

## Ticket 14

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `POST /containers/create` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `Mounts` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `HostConfig` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `Binds` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `Volumes` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `Tmpfs` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 38 |  |

## Ticket 15

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is _unversioned_ and applied to all API versions. | 39 | * `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is _unversioned_ and applied to all API versions. |
| affected_surface | `POST /build` | 39 | * `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is _unversioned_ and applied to all API versions. |
| affected_surface | `Dockerfile` | 39 | * `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is _unversioned_ and applied to all API versions. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 39 |  |

## Ticket 16

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` accepts `cachefrom` parameter to specify images used for build cache. | 40 | * `POST /build` accepts `cachefrom` parameter to specify images used for build cache. |
| affected_surface | `POST /build` | 40 | * `POST /build` accepts `cachefrom` parameter to specify images used for build cache. |
| affected_surface | `cachefrom` | 40 | * `POST /build` accepts `cachefrom` parameter to specify images used for build cache. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 40 |  |

## Ticket 17

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/` endpoint now correctly returns a list of *all* networks, | 41 | * `GET /networks/` endpoint now correctly returns a list of *all* networks, |
| affected_surface | `GET /networks/` | 41 | * `GET /networks/` endpoint now correctly returns a list of *all* networks, |
| affected_surface | `name` | 42 | instead of the default network if a trailing slash is provided, but no `name` |
| affected_surface | `id` | 43 | or `id`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 41-43 |  |

## Ticket 18

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress. | 44 | * `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress. |
| affected_surface | `DELETE /containers/(name)` | 44 | * `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress. |
| affected_surface | `removal of container name is already in progress` | 44 | * `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 44 |  |

## Ticket 19

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now supports a `is-task` filter to filter | 45 | * `GET /containers/json` now supports a `is-task` filter to filter |
| affected_surface | `GET /containers/json` | 45 | * `GET /containers/json` now supports a `is-task` filter to filter |
| affected_surface | `is-task` | 45 | * `GET /containers/json` now supports a `is-task` filter to filter |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 45-46 |  |

## Ticket 20

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `StopTimeout` field. | 47 | * `POST /containers/create` now takes `StopTimeout` field. |
| affected_surface | `POST /containers/create` | 47 | * `POST /containers/create` now takes `StopTimeout` field. |
| affected_surface | `StopTimeout` | 47 | * `POST /containers/create` now takes `StopTimeout` field. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 47 |  |

## Ticket 21

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| affected_surface | `POST /services/create` | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| affected_surface | `POST /services/(id or name)/update` | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| affected_surface | `Monitor` | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| affected_surface | `MaxFailureRatio` | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 48 |  |

## Ticket 22

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. | 49 | * `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. |
| affected_surface | `POST /services/(id or name)/update` | 49 | * `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. |
| affected_surface | `ForceUpdate` | 49 | * `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. |
| affected_surface | `TaskTemplate` | 49 | * `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 49 |  |

## Ticket 23

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. | 50 | * `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. |
| affected_surface | `POST /services/create` | 50 | * `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. |
| affected_surface | `POST /services/(id or name)/update` | 50 | * `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. |
| affected_surface | `Warnings` | 50 | * `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 50 |  |

## Ticket 24

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(name)` now returns field `Created` in response to show network created time. | 51 | * `GET /networks/(name)` now returns field `Created` in response to show network created time. |
| affected_surface | `GET /networks/(name)` | 51 | * `GET /networks/(name)` now returns field `Created` in response to show network created time. |
| affected_surface | returns | 51 | * `GET /networks/(name)` now returns field `Created` in response to show network created time. |
| affected_surface | `Created` | 51 | * `GET /networks/(name)` now returns field `Created` in response to show network created time. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 51 |  |

## Ticket 25

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution. | 52 | * `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution. |
| affected_surface | `POST /containers/(id or name)/exec` | 52 | * `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution. |
| affected_surface | `Env` | 52 | * `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 52 |  |

## Ticket 26

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| affected_surface | `GET /volumes` | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| affected_surface | `GET /volumes/(name)` | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| affected_surface | `POST /volumes/create` | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| affected_surface | `Options` | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 53 |  |

## Ticket 27

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process. | 54 | * `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process. |
| affected_surface | `GET /exec/(id)/json` | 54 | * `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process. |
| affected_surface | `Pid` | 54 | * `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 54 |  |

## Ticket 28

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/prune` prunes stopped containers. | 55 | * `POST /containers/prune` prunes stopped containers. |
| affected_surface | `POST /containers/prune` | 55 | * `POST /containers/prune` prunes stopped containers. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 55 |  |

## Ticket 29

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /images/prune` prunes unused images. | 56 | * `POST /images/prune` prunes unused images. |
| affected_surface | `POST /images/prune` | 56 | * `POST /images/prune` prunes unused images. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 56 |  |

## Ticket 30

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /volumes/prune` prunes unused volumes. | 57 | * `POST /volumes/prune` prunes unused volumes. |
| affected_surface | `POST /volumes/prune` | 57 | * `POST /volumes/prune` prunes unused volumes. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 57 |  |

## Ticket 31

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/prune` prunes unused networks. | 58 | * `POST /networks/prune` prunes unused networks. |
| affected_surface | `POST /networks/prune` | 58 | * `POST /networks/prune` prunes unused networks. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 58 |  |

## Ticket 32

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). | 59 | * Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). |
| affected_surface | `Docker-Experimental` | 59 | * Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). |
| affected_surface | `true` | 59 | * Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). |
| affected_surface | `false` | 59 | * Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 59 |  |

## Ticket 33

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Every API response now includes a `API-Version` header specifying the default API version of the server. | 60 | * Every API response now includes a `API-Version` header specifying the default API version of the server. |
| affected_surface | `API-Version` | 60 | * Every API response now includes a `API-Version` header specifying the default API version of the server. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 60 |  |

## Ticket 34

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| affected_surface | `hostConfig` | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| affected_surface | `CpuRealtimePeriod` | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| affected_surface | `CpuRtRuntime` | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| affected_surface | `CONFIG_RT_GROUP_SCHED` | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 61 |  |

## Ticket 35

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. | 62 | * The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. |
| affected_surface | `SecurityOptions` | 62 | * The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. |
| affected_surface | `GET /info` | 62 | * The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. |
| affected_surface | `userns` | 62 | * The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 62 |  |

## Ticket 36

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| affected_surface | `GET /nodes` | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| affected_surface | `GET /node/(id or name)` | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| affected_surface | `Addr` | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| affected_surface | `Status` | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 63 |  |

## Ticket 37

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `HostConfig` field now includes `NanoCPUs` that represents CPU quota in units of 10<sup>-9</sup> CPUs. | 64 | * The `HostConfig` field now includes `NanoCPUs` that represents CPU quota in units of 10<sup>-9</sup> CPUs. |
| affected_surface | `HostConfig` | 64 | * The `HostConfig` field now includes `NanoCPUs` that represents CPU quota in units of 10<sup>-9</sup> CPUs. |
| affected_surface | `NanoCPUs` | 64 | * The `HostConfig` field now includes `NanoCPUs` that represents CPU quota in units of 10<sup>-9</sup> CPUs. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 64 |  |

## Ticket 38

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns more structured information about security options. | 65 | * `GET /info` now returns more structured information about security options. |
| affected_surface | `GET /info` | 65 | * `GET /info` now returns more structured information about security options. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 65 |  |

## Ticket 39

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only. | 66 | * The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only. |
| affected_surface | `HostConfig` | 66 | * The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only. |
| affected_surface | `CpuCount` | 66 | * The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 66 |  |

## Ticket 40

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. | 67 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. |
| affected_surface | `POST /services/create` | 67 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. |
| affected_surface | `POST /services/(id or name)/update` | 67 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. |
| affected_surface | `TTY` | 67 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 67 |  |

## Ticket 41

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `POST /services/create` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `POST /services/(id or name)/update` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `DNSConfig` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `Nameservers` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `Search` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `Options` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 68 |  |

## Ticket 42

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(id or name)` now includes IP and name of all peers nodes for swarm mode overlay networks. | 69 | * `GET /networks/(id or name)` now includes IP and name of all peers nodes for swarm mode overlay networks. |
| affected_surface | `GET /networks/(id or name)` | 69 | * `GET /networks/(id or name)` now includes IP and name of all peers nodes for swarm mode overlay networks. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 69 |  |

## Ticket 43

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /plugins` list plugins. | 70 | * `GET /plugins` list plugins. |
| affected_surface | `GET /plugins` | 70 | * `GET /plugins` list plugins. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 70 |  |

## Ticket 44

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/pull?name=<plugin name>` pulls a plugin. | 71 | * `POST /plugins/pull?name=<plugin name>` pulls a plugin. |
| affected_surface | `POST /plugins/pull?name=<plugin name>` | 71 | * `POST /plugins/pull?name=<plugin name>` pulls a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 71 |  |

## Ticket 45

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /plugins/(plugin name)` inspect a plugin. | 72 | * `GET /plugins/(plugin name)` inspect a plugin. |
| affected_surface | `GET /plugins/(plugin name)` | 72 | * `GET /plugins/(plugin name)` inspect a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 72 |  |

## Ticket 46

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/set` configure a plugin. | 73 | * `POST /plugins/(plugin name)/set` configure a plugin. |
| affected_surface | `POST /plugins/(plugin name)/set` | 73 | * `POST /plugins/(plugin name)/set` configure a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 73 |  |

## Ticket 47

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/enable` enable a plugin. | 74 | * `POST /plugins/(plugin name)/enable` enable a plugin. |
| affected_surface | `POST /plugins/(plugin name)/enable` | 74 | * `POST /plugins/(plugin name)/enable` enable a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 74 |  |

## Ticket 48

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/disable` disable a plugin. | 75 | * `POST /plugins/(plugin name)/disable` disable a plugin. |
| affected_surface | `POST /plugins/(plugin name)/disable` | 75 | * `POST /plugins/(plugin name)/disable` disable a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 75 |  |

## Ticket 49

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/push` push a plugin. | 76 | * `POST /plugins/(plugin name)/push` push a plugin. |
| affected_surface | `POST /plugins/(plugin name)/push` | 76 | * `POST /plugins/(plugin name)/push` push a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 76 |  |

## Ticket 50

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/create?name=(plugin name)` create a plugin. | 77 | * `POST /plugins/create?name=(plugin name)` create a plugin. |
| affected_surface | `POST /plugins/create?name=(plugin name)` | 77 | * `POST /plugins/create?name=(plugin name)` create a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 77 |  |

## Ticket 51

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /plugins/(plugin name)` delete a plugin. | 78 | * `DELETE /plugins/(plugin name)` delete a plugin. |
| affected_surface | `DELETE /plugins/(plugin name)` | 78 | * `DELETE /plugins/(plugin name)` delete a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 78 |  |

## Ticket 52

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. | 79 | * `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. |
| affected_surface | `POST /node/(id or name)/update` | 79 | * `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. |
| affected_surface | `id` | 79 | * `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. |
| affected_surface | `name` | 79 | * `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 79 |  |

## Ticket 53

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/json` now support a `reference` filter. | 80 | * `GET /images/json` now support a `reference` filter. |
| affected_surface | `GET /images/json` | 80 | * `GET /images/json` now support a `reference` filter. |
| affected_surface | `reference` | 80 | * `GET /images/json` now support a `reference` filter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 80 |  |

## Ticket 54

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /secrets` returns information on the secrets. | 81 | * `GET /secrets` returns information on the secrets. |
| affected_surface | `GET /secrets` | 81 | * `GET /secrets` returns information on the secrets. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 81 |  |

## Ticket 55

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /secrets/create` creates a secret. | 82 | * `POST /secrets/create` creates a secret. |
| affected_surface | `POST /secrets/create` | 82 | * `POST /secrets/create` creates a secret. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 82 |  |

## Ticket 56

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /secrets/{id}` removes the secret `id`. | 83 | * `DELETE /secrets/{id}` removes the secret `id`. |
| affected_surface | `DELETE /secrets/{id}` | 83 | * `DELETE /secrets/{id}` removes the secret `id`. |
| affected_surface | `id` | 83 | * `DELETE /secrets/{id}` removes the secret `id`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 83 |  |

## Ticket 57

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /secrets/{id}` returns information on the secret `id`. | 84 | * `GET /secrets/{id}` returns information on the secret `id`. |
| affected_surface | `GET /secrets/{id}` | 84 | * `GET /secrets/{id}` returns information on the secret `id`. |
| affected_surface | `id` | 84 | * `GET /secrets/{id}` returns information on the secret `id`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 84 |  |

## Ticket 58

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /secrets/{id}/update` updates the secret `id`. | 85 | * `POST /secrets/{id}/update` updates the secret `id`. |
| affected_surface | `POST /secrets/{id}/update` | 85 | * `POST /secrets/{id}/update` updates the secret `id`. |
| affected_surface | `id` | 85 | * `POST /secrets/{id}/update` updates the secret `id`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 85 |  |

## Ticket 59

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter. | 86 | * `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter. |
| affected_surface | `POST /services/(id or name)/update` | 86 | * `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter. |
| affected_surface | a | 86 | * `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 86 |  |

## Ticket 60

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `StorageOpt` field. | 92 | * `POST /containers/create` now takes `StorageOpt` field. |
| affected_surface | `POST /containers/create` | 92 | * `POST /containers/create` now takes `StorageOpt` field. |
| affected_surface | `StorageOpt` | 92 | * `POST /containers/create` now takes `StorageOpt` field. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 92 |  |

## Ticket 61

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `GET /info` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `SecurityOptions` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `apparmor` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `seccomp` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `selinux` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 93 |  |

## Ticket 62

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration | 94 | * `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration |
| affected_surface | `GET /info` | 94 | * `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration |
| affected_surface | `ExecutionDriver` | 94 | * `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 94-95 |  |

## Ticket 63

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks` now supports filtering by `label` and `driver`. | 96 | * `GET /networks` now supports filtering by `label` and `driver`. |
| affected_surface | `GET /networks` | 96 | * `GET /networks` now supports filtering by `label` and `driver`. |
| affected_surface | `label` | 96 | * `GET /networks` now supports filtering by `label` and `driver`. |
| affected_surface | `driver` | 96 | * `GET /networks` now supports filtering by `label` and `driver`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 96 |  |

## Ticket 64

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now supports filtering containers by `network` name or id. | 97 | * `GET /containers/json` now supports filtering containers by `network` name or id. |
| affected_surface | `GET /containers/json` | 97 | * `GET /containers/json` now supports filtering containers by `network` name or id. |
| affected_surface | `network` | 97 | * `GET /containers/json` now supports filtering containers by `network` name or id. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 97 |  |

## Ticket 65

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. | 98 | * `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. |
| affected_surface | `POST /containers/create` | 98 | * `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. |
| affected_surface | `IOMaximumBandwidth` | 98 | * `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. |
| affected_surface | `IOMaximumIOps` | 98 | * `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 98 |  |

## Ticket 66

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now returns an HTTP 400 "bad parameter" message | 99 | * `POST /containers/create` now returns an HTTP 400 "bad parameter" message |
| affected_surface | `POST /containers/create` | 99 | * `POST /containers/create` now returns an HTTP 400 "bad parameter" message |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 99-100 |  |

## Ticket 67

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/search` now takes a `filters` query parameter. | 101 | * `GET /images/search` now takes a `filters` query parameter. |
| affected_surface | `GET /images/search` | 101 | * `GET /images/search` now takes a `filters` query parameter. |
| affected_surface | `filters` | 101 | * `GET /images/search` now takes a `filters` query parameter. |
| affected_surface | query | 101 | * `GET /images/search` now takes a `filters` query parameter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 101 |  |

## Ticket 68

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded. | 102 | * `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded. |
| affected_surface | `GET /events` | 102 | * `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded. |
| affected_surface | `reload` | 102 | * `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 102 |  |

## Ticket 69

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports filtering by daemon name or ID. | 103 | * `GET /events` now supports filtering by daemon name or ID. |
| affected_surface | `GET /events` | 103 | * `GET /events` now supports filtering by daemon name or ID. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 103 |  |

## Ticket 70

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports a `detach` event that is emitted on detaching from container process. | 104 | * `GET /events` now supports a `detach` event that is emitted on detaching from container process. |
| affected_surface | `GET /events` | 104 | * `GET /events` now supports a `detach` event that is emitted on detaching from container process. |
| affected_surface | `detach` | 104 | * `GET /events` now supports a `detach` event that is emitted on detaching from container process. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 104 |  |

## Ticket 71

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports an `exec_detach ` event that is emitted on detaching from exec process. | 105 | * `GET /events` now supports an `exec_detach ` event that is emitted on detaching from exec process. |
| affected_surface | `GET /events` | 105 | * `GET /events` now supports an `exec_detach ` event that is emitted on detaching from exec process. |
| affected_surface | `exec_detach ` | 105 | * `GET /events` now supports an `exec_detach ` event that is emitted on detaching from exec process. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 105 |  |

## Ticket 72

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/json` now supports filters `since` and `before`. | 106 | * `GET /images/json` now supports filters `since` and `before`. |
| affected_surface | `GET /images/json` | 106 | * `GET /images/json` now supports filters `since` and `before`. |
| affected_surface | `since` | 106 | * `GET /images/json` now supports filters `since` and `before`. |
| affected_surface | `before` | 106 | * `GET /images/json` now supports filters `since` and `before`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 106 |  |

## Ticket 73

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(id or name)/start` no longer accepts a `HostConfig`. | 107 | * `POST /containers/(id or name)/start` no longer accepts a `HostConfig`. |
| affected_surface | `POST /containers/(id or name)/start` | 107 | * `POST /containers/(id or name)/start` no longer accepts a `HostConfig`. |
| affected_surface | `HostConfig` | 107 | * `POST /containers/(id or name)/start` no longer accepts a `HostConfig`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 107 |  |

## Ticket 74

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /images/(name)/tag` no longer has a `force` query parameter. | 108 | * `POST /images/(name)/tag` no longer has a `force` query parameter. |
| affected_surface | `POST /images/(name)/tag` | 108 | * `POST /images/(name)/tag` no longer has a `force` query parameter. |
| affected_surface | `force` | 108 | * `POST /images/(name)/tag` no longer has a `force` query parameter. |
| affected_surface | query | 108 | * `POST /images/(name)/tag` no longer has a `force` query parameter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 108 |  |

## Ticket 75

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/search` now supports maximum returned search results `limit`. | 109 | * `GET /images/search` now supports maximum returned search results `limit`. |
| affected_surface | `GET /images/search` | 109 | * `GET /images/search` now supports maximum returned search results `limit`. |
| affected_surface | `limit` | 109 | * `GET /images/search` now supports maximum returned search results `limit`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 109 |  |

## Ticket 76

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. | 110 | * `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. |
| affected_surface | `POST /containers/{name:.*}/copy` | 110 | * `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. | 110 | * `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 110 |  |

## Ticket 77

| field | value | line | quote |
| --- | --- | --- | --- |
| change | API errors are now returned as JSON instead of plain text. | 111 | * API errors are now returned as JSON instead of plain text. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 111 |  |

## Ticket 78

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container. | 112 | * `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container. |
| affected_surface | `POST /containers/create` | 112 | * `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container. |
| affected_surface | `POST /containers/(id)/start` | 112 | * `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 112 |  |

## Ticket 79

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start` | 113 | * `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start` |
| affected_surface | `POST /containers/<container ID>/exec` | 113 | * `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start` |
| affected_surface | `POST /exec/<exec ID>/start` | 113 | * `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start` |
| affected_surface | "Container" | 114 | no longer expects a "Container" field to be present. This property was not used |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 113-115 |  |

## Ticket 80

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create/` now validates the hostname (should be a valid RFC 1123 hostname). | 116 | * `POST /containers/create/` now validates the hostname (should be a valid RFC 1123 hostname). |
| affected_surface | `POST /containers/create/` | 116 | * `POST /containers/create/` now validates the hostname (should be a valid RFC 1123 hostname). |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 116 |  |

## Ticket 81

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, | 117 | * `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, |
| affected_surface | `POST /containers/create/` | 117 | * `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, |
| affected_surface | `HostConfig.PidMode` | 117 | * `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, |
| affected_surface | `container:<name\|id>` | 117 | * `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 117-118 |  |

## Ticket 82

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `GET /containers/json` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `created` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `restarting` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `running` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `paused` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `exited` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `dead` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 124 |  |

## Ticket 83

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` returns the mount points for the container. | 125 | * `GET /containers/json` returns the mount points for the container. |
| affected_surface | `GET /containers/json` | 125 | * `GET /containers/json` returns the mount points for the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 125 |  |

## Ticket 84

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not. | 126 | * `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not. |
| affected_surface | `GET /networks/(name)` | 126 | * `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not. |
| affected_surface | `Internal` | 126 | * `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 126 |  |

## Ticket 85

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not. | 127 | * `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not. |
| affected_surface | `GET /networks/(name)` | 127 | * `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not. |
| affected_surface | `EnableIPv6` | 127 | * `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 127 |  |

## Ticket 86

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(name)/update` now supports updating container's restart policy. | 128 | * `POST /containers/(name)/update` now supports updating container's restart policy. |
| affected_surface | `POST /containers/(name)/update` | 128 | * `POST /containers/(name)/update` now supports updating container's restart policy. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 128 |  |

## Ticket 87

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work). | 129 | * `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work). |
| affected_surface | `POST /networks/create` | 129 | * `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work). |
| affected_surface | `EnableIPv6` | 129 | * `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work). |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 129 |  |

## Ticket 88

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| affected_surface | `GET /info` | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| affected_surface | `CgroupDriver` | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| affected_surface | `cgroupfs` | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| affected_surface | `systemd` | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 130 |  |

## Ticket 89

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported. | 131 | * `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported. |
| affected_surface | `GET /info` | 131 | * `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported. |
| affected_surface | `KernelMemory` | 131 | * `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 131 |  |

## Ticket 90

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported. | 132 | * `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported. |
| affected_surface | `POST /containers/create` | 132 | * `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported. |
| affected_surface | `PidsLimit` | 132 | * `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 132 |  |

## Ticket 91

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported. | 133 | * `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported. |
| affected_surface | `GET /containers/(id or name)/stats` | 133 | * `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported. |
| affected_surface | `pids_stats` | 133 | * `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 133 |  |

## Ticket 92

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now allows you to override usernamespaces remapping and use privileged options for the container. | 134 | * `POST /containers/create` now allows you to override usernamespaces remapping and use privileged options for the container. |
| affected_surface | `POST /containers/create` | 134 | * `POST /containers/create` now allows you to override usernamespaces remapping and use privileged options for the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 134 |  |

## Ticket 93

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume. | 135 | * `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume. |
| affected_surface | `POST /containers/create` | 135 | * `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume. |
| affected_surface | `nocopy` | 135 | * `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 135 |  |

## Ticket 94

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /auth` now returns an `IdentityToken` when supported by a registry. | 136 | * `POST /auth` now returns an `IdentityToken` when supported by a registry. |
| affected_surface | `POST /auth` | 136 | * `POST /auth` now returns an `IdentityToken` when supported by a registry. |
| affected_surface | `IdentityToken` | 136 | * `POST /auth` now returns an `IdentityToken` when supported by a registry. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 136 |  |

## Ticket 95

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| affected_surface | `POST /containers/create` | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| affected_surface | `Hostname` | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| affected_surface | `Domainname` | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| affected_surface | `Hostname.Domainname` | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 137 |  |

## Ticket 96

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /volumes` now supports more filters, new added filters are `name` and `driver`. | 138 | * `GET /volumes` now supports more filters, new added filters are `name` and `driver`. |
| affected_surface | `GET /volumes` | 138 | * `GET /volumes` now supports more filters, new added filters are `name` and `driver`. |
| affected_surface | `name` | 138 | * `GET /volumes` now supports more filters, new added filters are `name` and `driver`. |
| affected_surface | `driver` | 138 | * `GET /volumes` now supports more filters, new added filters are `name` and `driver`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 138 |  |

## Ticket 97

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| affected_surface | `GET /containers/(id or name)/logs` | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| affected_surface | `details` | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| affected_surface | query | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| affected_surface | `LogOpts` | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 139 |  |

## Ticket 98

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. | 140 | * `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. |
| affected_surface | `POST /images/load` | 140 | * `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. |
| affected_surface | `quiet` | 140 | * `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. |
| affected_surface | query | 140 | * `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 140 |  |

## Ticket 99

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /container/(name)/update` updates the resources of a container. | 146 | * `POST /container/(name)/update` updates the resources of a container. |
| affected_surface | `POST /container/(name)/update` | 146 | * `POST /container/(name)/update` updates the resources of a container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 146 |  |

## Ticket 100

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` supports filter `isolation` on Windows. | 147 | * `GET /containers/json` supports filter `isolation` on Windows. |
| affected_surface | `GET /containers/json` | 147 | * `GET /containers/json` supports filter `isolation` on Windows. |
| affected_surface | `isolation` | 147 | * `GET /containers/json` supports filter `isolation` on Windows. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 147 |  |

## Ticket 101

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now returns the list of networks of containers. | 148 | * `GET /containers/json` now returns the list of networks of containers. |
| affected_surface | `GET /containers/json` | 148 | * `GET /containers/json` now returns the list of networks of containers. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 148 |  |

## Ticket 102

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` Now returns `Architecture` and `OSType` fields, providing information | 149 | * `GET /info` Now returns `Architecture` and `OSType` fields, providing information |
| affected_surface | `GET /info` | 149 | * `GET /info` Now returns `Architecture` and `OSType` fields, providing information |
| affected_surface | `Architecture` | 149 | * `GET /info` Now returns `Architecture` and `OSType` fields, providing information |
| affected_surface | `OSType` | 149 | * `GET /info` Now returns `Architecture` and `OSType` fields, providing information |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 149-150 |  |

## Ticket 103

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(name)` now returns a `Name` field for each container attached to the network. | 151 | * `GET /networks/(name)` now returns a `Name` field for each container attached to the network. |
| affected_surface | `GET /networks/(name)` | 151 | * `GET /networks/(name)` now returns a `Name` field for each container attached to the network. |
| affected_surface | `Name` | 151 | * `GET /networks/(name)` now returns a `Name` field for each container attached to the network. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 151 |  |

## Ticket 104

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it | 152 | * `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it |
| affected_surface | `GET /version` | 152 | * `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it |
| affected_surface | `BuildTime` | 152 | * `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 152-153 |  |

## Ticket 105

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `AuthConfig` now supports a `registrytoken` for token based authentication | 154 | * `AuthConfig` now supports a `registrytoken` for token based authentication |
| affected_surface | `AuthConfig` | 154 | * `AuthConfig` now supports a `registrytoken` for token based authentication |
| affected_surface | `registrytoken` | 154 | * `AuthConfig` now supports a `registrytoken` for token based authentication |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 154 |  |

## Ticket 106

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory` | 155 | * `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory` |
| affected_surface | `POST /containers/create` | 155 | * `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory` |
| affected_surface | `HostConfig.KernelMemory` | 155 | * `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 155 |  |

## Ticket 107

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create` | 156 | * Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create` |
| affected_surface | `POST /images/(name)/push` | 156 | * Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create` |
| affected_surface | `POST /images/create` | 156 | * Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 156-158 |  |

## Ticket 108

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now allows you to set a read/write rate limit for a | 159 | * `POST /containers/create` now allows you to set a read/write rate limit for a |
| affected_surface | `POST /containers/create` | 159 | * `POST /containers/create` now allows you to set a read/write rate limit for a |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 159-160 |  |

## Ticket 109

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks` now supports filtering by `name`, `id` and `type`. | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| affected_surface | `GET /networks` | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| affected_surface | `name` | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| affected_surface | `id` | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| affected_surface | `type` | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 161 |  |

## Ticket 110

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now allows you to set the static IPv4 and/or IPv6 address for the container. | 162 | * `POST /containers/create` now allows you to set the static IPv4 and/or IPv6 address for the container. |
| affected_surface | `POST /containers/create` | 162 | * `POST /containers/create` now allows you to set the static IPv4 and/or IPv6 address for the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 162 |  |

## Ticket 111

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/(id)/connect` now allows you to set the static IPv4 and/or IPv6 address for the container. | 163 | * `POST /networks/(id)/connect` now allows you to set the static IPv4 and/or IPv6 address for the container. |
| affected_surface | `POST /networks/(id)/connect` | 163 | * `POST /networks/(id)/connect` now allows you to set the static IPv4 and/or IPv6 address for the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 163 |  |

## Ticket 112

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now includes the number of containers running, stopped, and paused. | 164 | * `GET /info` now includes the number of containers running, stopped, and paused. |
| affected_surface | `GET /info` | 164 | * `GET /info` now includes the number of containers running, stopped, and paused. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 164 |  |

## Ticket 113

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field. | 165 | * `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field. |
| affected_surface | `POST /networks/create` | 165 | * `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field. |
| affected_surface | `Internal` | 165 | * `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 165 |  |

## Ticket 114

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network | 166 | * `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network |
| affected_surface | `POST /networks/(id)/disconnect` | 166 | * `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network |
| affected_surface | `Force` | 166 | * `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 166 |  |

## Ticket 115

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/json` now returns the `NetworkID` of containers. | 167 | * `GET /containers/(id)/json` now returns the `NetworkID` of containers. |
| affected_surface | `GET /containers/(id)/json` | 167 | * `GET /containers/(id)/json` now returns the `NetworkID` of containers. |
| affected_surface | `NetworkID` | 167 | * `GET /containers/(id)/json` now returns the `NetworkID` of containers. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 167 |  |

## Ticket 116

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/create` Now supports an options field in the IPAM config that provides options | 168 | * `POST /networks/create` Now supports an options field in the IPAM config that provides options |
| affected_surface | `POST /networks/create` | 168 | * `POST /networks/create` Now supports an options field in the IPAM config that provides options |
| affected_surface | options | 168 | * `POST /networks/create` Now supports an options field in the IPAM config that provides options |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 168-169 |  |

## Ticket 117

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/{network-id}` Now returns IPAM config options for custom IPAM plugins if any | 170 | * `GET /networks/{network-id}` Now returns IPAM config options for custom IPAM plugins if any |
| affected_surface | `GET /networks/{network-id}` | 170 | * `GET /networks/{network-id}` Now returns IPAM config options for custom IPAM plugins if any |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 170-171 |  |

## Ticket 118

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/<network-id>` now returns subnets info for user-defined networks. | 172 | * `GET /networks/<network-id>` now returns subnets info for user-defined networks. |
| affected_surface | `GET /networks/<network-id>` | 172 | * `GET /networks/<network-id>` now returns subnets info for user-defined networks. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 172 |  |

## Ticket 119

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications | 173 | * `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications |
| affected_surface | `GET /info` | 173 | * `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications |
| affected_surface | `SystemStatus` | 173 | * `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 173-174 |  |

## Ticket 120

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /volumes` lists volumes from all volume drivers. | 180 | * `GET /volumes` lists volumes from all volume drivers. |
| affected_surface | `GET /volumes` | 180 | * `GET /volumes` lists volumes from all volume drivers. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 180 |  |

## Ticket 121

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /volumes/create` to create a volume. | 181 | * `POST /volumes/create` to create a volume. |
| affected_surface | `POST /volumes/create` | 181 | * `POST /volumes/create` to create a volume. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 181 |  |

## Ticket 122

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /volumes/(name)` get low-level information about a volume. | 182 | * `GET /volumes/(name)` get low-level information about a volume. |
| affected_surface | `GET /volumes/(name)` | 182 | * `GET /volumes/(name)` get low-level information about a volume. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 182 |  |

## Ticket 123

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /volumes/(name)` remove a volume with the specified name. | 183 | * `DELETE /volumes/(name)` remove a volume with the specified name. |
| affected_surface | `DELETE /volumes/(name)` | 183 | * `DELETE /volumes/(name)` remove a volume with the specified name. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 183 |  |

## Ticket 124

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. | 184 | * `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. |
| affected_surface | `VolumeDriver` | 184 | * `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. |
| affected_surface | `config` | 184 | * `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. |
| affected_surface | `HostConfig` | 184 | * `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 184 |  |

## Ticket 125

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. | 185 | * `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. |
| affected_surface | `GET /images/(name)/json` | 185 | * `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. |
| affected_surface | `RepoTags` | 185 | * `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. |
| affected_surface | `RepoDigests` | 185 | * `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 185 |  |

## Ticket 126

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. | 186 | * The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. |
| affected_surface | `config` | 186 | * The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. |
| affected_surface | the | 186 | * The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. |
| affected_surface | `StopSignal` | 186 | * The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 186 |  |

## Ticket 127

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/stats` will return networking information respectively for each interface. | 187 | * `GET /containers/(id)/stats` will return networking information respectively for each interface. |
| affected_surface | `GET /containers/(id)/stats` | 187 | * `GET /containers/(id)/stats` will return networking information respectively for each interface. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 187 |  |

## Ticket 128

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options. | 188 | * The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options. |
| affected_surface | `HostConfig` | 188 | * The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options. |
| affected_surface | `DnsOptions` | 188 | * The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 188 |  |

## Ticket 129

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` now optionally takes a serialized map of build-time variables. | 189 | * `POST /build` now optionally takes a serialized map of build-time variables. |
| affected_surface | `POST /build` | 189 | * `POST /build` now optionally takes a serialized map of build-time variables. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 189 |  |

## Ticket 130

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now includes a `timenano` field, in addition to the existing `time` field. | 190 | * `GET /events` now includes a `timenano` field, in addition to the existing `time` field. |
| affected_surface | `GET /events` | 190 | * `GET /events` now includes a `timenano` field, in addition to the existing `time` field. |
| affected_surface | `timenano` | 190 | * `GET /events` now includes a `timenano` field, in addition to the existing `time` field. |
| affected_surface | `time` | 190 | * `GET /events` now includes a `timenano` field, in addition to the existing `time` field. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 190 |  |

## Ticket 131

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports filtering by image and container labels. | 191 | * `GET /events` now supports filtering by image and container labels. |
| affected_surface | `GET /events` | 191 | * `GET /events` now supports filtering by image and container labels. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 191 |  |

## Ticket 132

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. | 192 | * `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. |
| affected_surface | `GET /info` | 192 | * `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. |
| affected_surface | `CPUShares` | 192 | * `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. |
| affected_surface | `Cpuset` | 192 | * `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 192 |  |

## Ticket 133

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` will return `ImageID` of the image used by container. | 193 | * `GET /containers/json` will return `ImageID` of the image used by container. |
| affected_surface | `GET /containers/json` | 193 | * `GET /containers/json` will return `ImageID` of the image used by container. |
| affected_surface | `ImageID` | 193 | * `GET /containers/json` will return `ImageID` of the image used by container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 193 |  |

## Ticket 134

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /exec/(name)/start` will now return an HTTP 409 when the container is either stopped or paused. | 194 | * `POST /exec/(name)/start` will now return an HTTP 409 when the container is either stopped or paused. |
| affected_surface | `POST /exec/(name)/start` | 194 | * `POST /exec/(name)/start` will now return an HTTP 409 when the container is either stopped or paused. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 194 |  |

## Ticket 135

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit. | 195 | * `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit. |
| affected_surface | `POST /containers/create` | 195 | * `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit. |
| affected_surface | `KernelMemory` | 195 | * `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 195 |  |

## Ticket 136

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | `GET /containers/(name)/json` | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | `size` | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | this | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | `SizeRw` | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | `SizeRootFs` | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 196 |  |

## Ticket 137

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field, | 197 | * `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | `GET /containers/(name)/json` | 197 | * `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | `NetworkSettings.Networks` | 197 | * `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | This | 198 | detailing network settings per network. This field deprecates the |
| affected_surface | `NetworkSettings.Gateway` | 199 | `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`, |
| affected_surface | `NetworkSettings.IPAddress` | 199 | `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`, |
| affected_surface | `NetworkSettings.IPPrefixLen` | 200 | `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which |
| affected_surface | `NetworkSettings.MacAddress` | 200 | `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | are still returned for backward-compatibility, but will be removed in a future version. | 201 | are still returned for backward-compatibility, but will be removed in a future version. |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 197-201 |  |

## Ticket 138

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field, | 202 | * `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | `GET /exec/(id)/json` | 202 | * `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | `NetworkSettings.Networks` | 202 | * `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | This | 203 | detailing networksettings per network. This field deprecates the |
| affected_surface | `NetworkSettings.Gateway` | 204 | `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`, |
| affected_surface | `NetworkSettings.IPAddress` | 204 | `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`, |
| affected_surface | `NetworkSettings.IPPrefixLen` | 205 | `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which |
| affected_surface | `NetworkSettings.MacAddress` | 205 | `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | are still returned for backward-compatibility, but will be removed in a future version. | 206 | are still returned for backward-compatibility, but will be removed in a future version. |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 202-206 |  |

## Ticket 139

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the | 207 | * The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the |
| affected_surface | `HostConfig` | 207 | * The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the |
| affected_surface | `OomScoreAdj` | 207 | * The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 207-209 |  |

## Ticket 140

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/archive` get an archive of filesystem content from a container. | 215 | * `GET /containers/(id)/archive` get an archive of filesystem content from a container. |
| affected_surface | `GET /containers/(id)/archive` | 215 | * `GET /containers/(id)/archive` get an archive of filesystem content from a container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 215 |  |

## Ticket 141

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `PUT /containers/(id)/archive` upload an archive of content to be extracted to | 216 | * `PUT /containers/(id)/archive` upload an archive of content to be extracted to |
| affected_surface | `PUT /containers/(id)/archive` | 216 | * `PUT /containers/(id)/archive` upload an archive of content to be extracted to |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 216 |  |

## Ticket 142

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(id)/copy` is deprecated in favor of the above `archive` | 218 | * `POST /containers/(id)/copy` is deprecated in favor of the above `archive` |
| affected_surface | `POST /containers/(id)/copy` | 218 | * `POST /containers/(id)/copy` is deprecated in favor of the above `archive` |
| affected_surface | `archive` | 218 | * `POST /containers/(id)/copy` is deprecated in favor of the above `archive` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 218 |  |

## Ticket 143

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `hostConfig` option now accepts the field `GroupAdd`, which specifies a | 220 | * The `hostConfig` option now accepts the field `GroupAdd`, which specifies a |
| affected_surface | `hostConfig` | 220 | * The `hostConfig` option now accepts the field `GroupAdd`, which specifies a |
| affected_surface | the | 220 | * The `hostConfig` option now accepts the field `GroupAdd`, which specifies a |
| affected_surface | `GroupAdd` | 220 | * The `hostConfig` option now accepts the field `GroupAdd`, which specifies a |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 220 |  |

## Ticket 144

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect. | 230 | * `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect. |
| affected_surface | `GET /containers/(id)/stats` | 230 | * `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect. |
| affected_surface | `stream` | 230 | * `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 230 |  |

## Ticket 145

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. | 231 | * `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. |
| affected_surface | `GET /containers/(id)/logs` | 231 | * `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. |
| affected_surface | `since` | 231 | * `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. |
| affected_surface | timestamp | 231 | * `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 231 |  |

## Ticket 146

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` | 236 | * The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` |
| affected_surface | `hostConfig` | 236 | * The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` |
| affected_surface | `CpuPeriod` | 236 | * The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` |
| affected_surface | `CpuQuota` | 236 | * The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 236 |  |

## Ticket 147

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` accepts `cpuperiod` and `cpuquota` options | 237 | * `POST /build` accepts `cpuperiod` and `cpuquota` options |
| affected_surface | `POST /build` | 237 | * `POST /build` accepts `cpuperiod` and `cpuquota` options |
| affected_surface | `cpuperiod` | 237 | * `POST /build` accepts `cpuperiod` and `cpuquota` options |
| affected_surface | `cpuquota` | 237 | * `POST /build` accepts `cpuperiod` and `cpuquota` options |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 237 |  |

## Ticket 148

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /version` now returns `Os`, `Arch` and `KernelVersion`. | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| affected_surface | `GET /version` | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| affected_surface | `Os` | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| affected_surface | `Arch` | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| affected_surface | `KernelVersion` | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 243 |  |

## Ticket 149

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` and `POST /containers/(id)/start`allow you to  set ulimit settings for use in the container. | 244 | * `POST /containers/create` and `POST /containers/(id)/start`allow you to  set ulimit settings for use in the container. |
| affected_surface | `POST /containers/create` | 244 | * `POST /containers/create` and `POST /containers/(id)/start`allow you to  set ulimit settings for use in the container. |
| affected_surface | `POST /containers/(id)/start` | 244 | * `POST /containers/create` and `POST /containers/(id)/start`allow you to  set ulimit settings for use in the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 244 |  |

## Ticket 150

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `GET /info` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `SystemTime` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `HttpProxy` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `HttpsProxy` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `NoProxy` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 245 |  |

## Ticket 151

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/json` added a `RepoDigests` field to include image digest information. | 246 | * `GET /images/json` added a `RepoDigests` field to include image digest information. |
| affected_surface | `GET /images/json` | 246 | * `GET /images/json` added a `RepoDigests` field to include image digest information. |
| affected_surface | `RepoDigests` | 246 | * `GET /images/json` added a `RepoDigests` field to include image digest information. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 246 |  |

## Ticket 152

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` can now set resource constraints for all containers created for the build. | 247 | * `POST /build` can now set resource constraints for all containers created for the build. |
| affected_surface | `POST /build` | 247 | * `POST /build` can now set resource constraints for all containers created for the build. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 247 |  |

## Ticket 153

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `CgroupParent` can be passed in the host config to setup container cgroups under a specific cgroup. | 248 | * `CgroupParent` can be passed in the host config to setup container cgroups under a specific cgroup. |
| affected_surface | `CgroupParent` | 248 | * `CgroupParent` can be passed in the host config to setup container cgroups under a specific cgroup. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 248 |  |

## Ticket 154

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` closing the HTTP request cancels the build | 249 | * `POST /build` closing the HTTP request cancels the build |
| affected_surface | `POST /build` | 249 | * `POST /build` closing the HTTP request cancels the build |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 249 |  |

## Ticket 155

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(id)/exec` includes `Warnings` field to response. | 250 | * `POST /containers/(id)/exec` includes `Warnings` field to response. |
| affected_surface | `POST /containers/(id)/exec` | 250 | * `POST /containers/(id)/exec` includes `Warnings` field to response. |
| affected_surface | `Warnings` | 250 | * `POST /containers/(id)/exec` includes `Warnings` field to response. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 250 |  |

## Unmapped

- 1: ---
- 2: title: "Engine API version history"
- 3: description: "Documentation of changes that have been made to Engine API."
- 4: keywords: "API, Docker, rcli, REST, documentation"
- 5: ---
- 7: <!-- This file is maintained within the docker/docker Github
- 8:      repository at https://github.com/docker/docker/. Make all
- 9:      pull requests against that repo. If you see this file in
- 10:      another repository, consider it read-only there, as it will
- 11:      periodically be overwritten by the definitive file. Pull
- 12:      requests which include edits to this file in other repositories
- 13:      will be rejected.
- 14: -->
- 16: ## v1.26 API changes
- 18: [Docker Engine API v1.26](https://docs.docker.com/engine/api/v1.26/) documentation
- 22: ## v1.25 API changes
- 24: [Docker Engine API v1.25](https://docs.docker.com/engine/api/v1.25/) documentation
- 46:   containers that are tasks (part of a service in swarm mode).
- 88: ## v1.24 API changes
- 90: [Docker Engine API v1.24](v1.24.md) documentation
- 95:   with ContainerD in Docker 1.11.
- 100:   if no command is specified (instead of an HTTP 500 "server error")
- 115:   and is no longer sent by the docker client.
- 118:   to have the container join the PID namespace of an existing container.
- 120: ## v1.23 API changes
- 122: [Docker Engine API v1.23](v1.23.md) documentation
- 142: ## v1.22 API changes
- 144: [Docker Engine API v1.22](v1.22.md) documentation
- 150:   about the host architecture and operating system type that the daemon runs on.
- 153:   consistent with other date/time values returned by the API.
- 157:   will be cancelled if the HTTP connection making the API request is closed before
- 158:   the push or pull completes.
- 160:   device (in bytes per second or IO per second).
- 169:   for custom IPAM plugins.
- 171:   are available.
- 174:   that are built on top of engine.
- 176: ## v1.21 API changes
- 178: [Docker Engine API v1.21](v1.21.md) documentation
- 208:   badness heuristic. This heuristic selects which processes the OOM killer kills
- 209:   under out-of-memory conditions.
- 211: ## v1.20 API changes
- 213: [Docker Engine API v1.20](v1.20.md) documentation
- 217: an existing directory inside a container's filesystem.
- 219: endpoint which can be used to download files and directories from a container.
- 221: list of additional groups that the container process will run as.
- 223: ## v1.19 API changes
- 225: [Docker Engine API v1.19](v1.19.md) documentation
- 227: * When the daemon detects a version mismatch with the client, usually when
- 228: the client is newer than the daemon, an HTTP 400 is now returned instead
- 229: of a 404.
- 232: * `GET /info` The fields `Debug`, `IPv4Forwarding`, `MemoryLimit`, and
- 233: `SwapLimit` are now returned as boolean instead of as an int. In addition, the
- 234: end point now returns the new boolean fields `CpuCfsPeriod`, `CpuCfsQuota`, and
- 235: `OomKillDisable`.
- 239: ## v1.18 API changes
- 241: [Docker Engine API v1.18](v1.18.md) documentation
