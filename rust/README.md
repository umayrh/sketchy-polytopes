# Rust Projects

## Intro

To install Rust, see [rustup](https://rustup.rs). This will likely install all binaries
under `$HOME/.cargo/bin`, so this path must be added to `PATH`.

To build using the Gradle Rust plugin,
* Ensure that the project structure follows the expected 
[structure](https://ysb33rorg.gitlab.io/rust-gradle-plugin/0.2/docs/product-documentation.html). E.g.
```src
   ├── bench
   │   └── rust
   ├── main
   │   └── rust
   │       └── main.rs
   └── test
       └── rust
```
* Ensure that a valid Cargo.toml exists for the project. In particular, that the
package version in there and in build.gradle follows [semantic versioning](https://semver.org).
* `gradle build`: compiles the main and test code
* `gradle runApp`: runs the executable

To build in the traditional rust way (build artifacts will be under the `target` dir):
* Ensure that Cargo.toml has the `[[bin]]` block defined.
* `cargo build`
* `cargo run`

Issues:
* IntelliJ's plugin looks for a toolchain path different than what Rustup sets up. See
this [issue](https://github.com/intellij-rust/intellij-rust/issues/383).

## Rust

* [The Rust Programming Language](https://doc.rust-lang.org/book/second-edition/foreword.html)

### Testing, style, documentation

* [Rust Style Guide](https://github.com/rust-lang-nursery/fmt-rfcs/blob/master/guide/guide.md#types)

### Building

* [Rust Gradle](https://ysb33rorg.gitlab.io/rust-gradle-plugin/0.2/docs/product-documentation.html)
* [Rust Exe Gradle](http://ysb33r.gitlab.io/NativeGradle/#_building_rust_executables)
* [Rust for Java Devs](https://lankydanblog.com/2018/01/21/rust-for-java-devs-compiling-code-and-using-cargo/)

### Packaging

* [Cargo](https://doc.rust-lang.org/stable/rust-by-example/cargo.html)
