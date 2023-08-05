pip3 uninstall @projname@
git rm -r dist
git rm -r build
git rm -r @projname@.egg-info
rm -r dist
rm -r build
rm -r @projname@.egg-info
git add .
git commit -m "remove old build"

