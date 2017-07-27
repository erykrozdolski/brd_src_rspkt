/*
 * grunt-brd_src_rspkt
 * https://github.com/erykrozdolski/brd_src_rspkt
 *
 * Copyright (c) 2017 Eryk Rozdolski
 * Licensed under the MIT license.
 */

'use strict';


module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);
  grunt.loadNpmTasks('grunt-bower');
  grunt.loadNpmTasks('grunt-wiredep');
  // Project configuration.
  grunt.initConfig({
    wiredep: {
      task: {
        src: [
          'web/templates/base.html',
        ],

        options: {
        }
      }
    },
    sass: {
        // this is the "dev" Sass config used with "grunt watch" command
        dev: {
            options: {
                includePaths: ['.sass/'],
                outputStyle: 'nested',
            },
            expand: true,
            cwd: 'sass',
            src: ["*.scss"],
            dest: "web/static/css",
            ext: ".css",
        },
        // this is the "production" Sass config used with the "grunt buildcss" command
        dist: {
            options: {
                includePaths: ['.sass/'],
                outputStyle: 'nested',
            },
            expand: true,
            cwd: 'sass',
            src: ["*.scss"],
            dest: "web/static/css",
            ext: ".css",
        },
    },
    jshint: {
      all: [
        'Gruntfile.js',
        'tasks/*.js',
        '<%= nodeunit.tests %>'
      ],
      options: {
        jshintrc: '.jshintrc'
      }
    },

    // Before generating any new files, remove any previously-created files.
    clean: {
      tests: ['tmp']
    },

    // Configuration to be run (and then tested).
    brd_src_rspkt: {
      default_options: {
        options: {
        },
        files: {
          'tmp/default_options': ['test/fixtures/testing', 'test/fixtures/123']
        }
      },
      custom_options: {
        options: {
          separator: ': ',
          punctuation: ' !!!'
        },
        files: {
          'tmp/custom_options': ['test/fixtures/testing', 'test/fixtures/123']
        }
      }
    },

    // Unit tests.
    nodeunit: {
      tests: ['test/*_test.js']
    },
    tsc: {
        options: {
            // global options
        },
        task_name: {
            options: {
            target:"ES6"
            },
            files: [{
                expand : true,
                dest   : "static/js",
                cwd    : "ts",
                ext    : ".js",
                src    : [
                    "*.ts",
                    "!*.d.ts"
                ]
            }]
        }
    },
    watch: {
        sass: {
            files: 'sass/*.scss',
            tasks: ['sass']
        },
    },
    bower: {
      dev: {
        dest: 'dest/',
        js_dest: 'dest/js',
        css_dest: 'dest/styles'
      }
    }
  });

  // Actually load this plugin's task(s).
  grunt.loadTasks('tasks');

  // These plugins provide necessary tasks.

  // Whenever the "test" task is run, first clean the "tmp" dir, then run this
  // plugin's task(s), then test the result.
  grunt.registerTask('test', ['clean', 'brd_src_rspkt', 'nodeunit']);

  // By default, lint and run all tests.
  grunt.registerTask('default', ['jshint', 'test']);
  grunt.registerTask('default', ['sass']);
  grunt.registerTask('default', ['tsc']);
  grunt.registerTask('default', ['watch']);
  grunt.registerTask('default', ['bower']);
  grunt.registerTask('default', ['wiredep']);


};
