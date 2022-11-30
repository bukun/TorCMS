git pull
podman run --rm -it -v `pwd`:/ws node:lts-alpine sh -c 'cd /ws && yarn'
podman run --rm -it -v `pwd`:/ws node:lts-alpine sh -c 'cd /ws && yarn add quasar'
podman run --rm -it -v `pwd`:/ws node:lts-alpine sh -c 'cd /ws && yarn quasar build'
