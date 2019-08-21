git config --local user.name "wangshijun"
git config --local user.email "wangshijun2010@gmail.com"

git remote remove origin
git remote add origin "https://$GITHUB_TOKEN@github.com/$TRAVIS_REPO_SLUG.git"
git remote -v
git pull origin feature-publish
git checkout feature-publish
git branch -a

DEBUG=* node tools/setup-ci.js

npm publish

# trigger cnpm sync
curl -X PUT https://npm.taobao.org/sync/forge-python-starter?sync_upstream=true
