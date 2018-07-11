# Travis CI

## Intro

See [Travis config](./.travis.yml) and the pre-install [script](./travis/travis-setup.sh).

## Issues

* [No Neo4j version support](https://github.com/travis-ci/travis-ci/issues/3243)
    * A build matrix would also require running parallel instances of Neo4j

## References

* [Build life-cycle](https://docs.travis-ci.com/user/customizing-the-build/#The-Build-Lifecycle)
* [Caching Dependencies and Directories](https://docs.travis-ci.com/user/caching)
* [Database Setup](https://docs.travis-ci.com/user/database-setup/)

* [Best Practices](https://eng.localytics.com/best-practices-and-common-mistakes-with-travis-ci/)
* [Faster CI](https://atchai.com/blog/faster-ci/)