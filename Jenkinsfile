pipeline {
  agent none
  stages {
    stage('Test') {
      agent {
        dockerfile {
          filename 'Dockerfile'
          label 'service-agent'
          args '--network internal'
        }
      }
      environment {
        REDIS_HOST = 'redis'
      }
      steps {
        sh 'cd /app && pytest doku/tests --junitxml=$WORKSPACE/TESTS.xml'
        junit 'TESTS.xml'
      }
    }
    stage('Build') {
      when {
        beforeAgent true
        anyOf {
          branch 'master'
        }
      }
      agent {
        label 'service-agent'
      }
      environment {
        REGISTRY = credentials('desklab-registry')
      }
      steps {
        sh 'docker build -t reg.desk-lab.de/doku -t reg.desk-lab.de/doku:$GIT_COMMIT .'
        sh 'cd doku/static && docker build -t reg.desk-lab.de/doku-static -t reg.desk-lab.de/doku-static:$GIT_COMMIT .'
        sh 'docker login https://reg.desk-lab.de --username $REGISTRY_USR --password $REGISTRY_PSW'
        sh 'docker push reg.desk-lab.de/doku-static'
        sh 'docker push reg.desk-lab.de/doku-static:$GIT_COMMIT'
        sh 'docker push reg.desk-lab.de/doku'
        sh 'docker push reg.desk-lab.de/doku:$GIT_COMMIT'
      }
    }
    stage('Deploy') {
      when {
        beforeAgent true
        anyOf {
          branch 'master'
        }
      }
      agent {
        label 'deploy-agent'
      }
      options { skipDefaultCheckout() }
      environment {
        REGISTRY = credentials('desklab-registry')
      }
      steps {
        sh 'docker login https://reg.desk-lab.de --username $REGISTRY_USR --password $REGISTRY_PSW'
        sh 'cd /home/jenkins/server && docker-compose pull doku dokustatic'
        sh 'cd /home/jenkins/server && docker-compose up -d doku dokustatic'
      }
    }
  }
}
