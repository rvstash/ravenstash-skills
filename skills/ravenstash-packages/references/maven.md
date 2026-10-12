# Maven workflows

Load for Maven, Java, JVM, Kotlin, Scala, coordinates, install, verify, or deploy work.

## Read and build

```bash
rvs mvn --rvs-target platform/packages verify
rvs mvn --rvs-target mirror:maven-central test
rvs mvn --rvs-target platform/packages dependency:get \
  -Dartifact=com.example:lib:1.0.0
```

Private mirrors support reads only. Maven remains responsible for the project model, dependency graph, lifecycle, and build output.

## Deploy

Deploy only to an exact private Maven repository:

```bash
rvs mvn --rvs-target platform/releases \
  org.apache.maven.plugins:maven-deploy-plugin:3.1.3:deploy-file \
  -Dfile=target/lib-1.0.0.jar \
  -DgroupId=com.example \
  -DartifactId=lib \
  -Dversion=1.0.0 \
  -Dpackaging=jar
```

Confirm the artifact checksum or build provenance available to the user, Maven coordinates, account, repository, and format before creating remote state.

## Settings

`rvs art endpoint --format maven` prints routing; `rvs art native config mvn` prints settings and commands without minting credentials or writing files. Persistent settings changes require explicit intent. Do not write a Ravenstash token into `settings.xml` or include it in build logs.
