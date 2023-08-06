# Contributing

We welcome pull requests from everyone who follows the project guidelines. By participating in this project, you agree to abide by the BoogieMobile [code of conduct].

[code of conduct]: https://github.com/BoogieMobile/boogiepi/blob/master/CODE_OF_CONDUCT.md

Fork, then clone the repo:

    git clone git@github.com:your-username/boogiepi.git

Set up your machine:

    ./bin/setup

Make sure the tests pass:

    rake

Make your change. Add tests for your change. Make the tests pass:

    rake

Push to your fork and [submit a pull request][pr].

[pr]: https://github.com/BoogieMobile/boogiepi/pull/new/master

At this point you're waiting on us. We like to at least comment on pull requests within one week (and, typically, three business days) We may suggest some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is accepted:

* Write [tests][testing].
* Properly [document][documentation] any code modified or added.
* Adhere to the [*Black* code style][style].
* Write a [good commit message][commit].


[testing]: https://realpython.com/python-testing/
[documentation]: https://devguide.python.org/documenting/
[style]: https://github.com/psf/black
[commit]: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html