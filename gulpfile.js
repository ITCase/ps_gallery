var autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    filter = require('gulp-filter'),
    mainBowerFiles = require('main-bower-files'),
    minifyCSS = require('gulp-minify-css'),
    watch = require('gulp-watch');

var _ = require("underscore"),
    browserify = require('browserify'),
    glob = require("glob"),
    minimatch = require("minimatch"),
    source = require('vinyl-source-stream');

function getFiles(path) {
    var files = glob.sync(path + '**/*.css');
    target = minimatch.match(files, '__*.css', { matchBase: true });
    ignore = _.map(target, function(item){ return '!' + item; });
    result = files.concat(mainBowerFiles()).concat(ignore);
    return result;
}

gulp.task('browserify', function() {
    browserify('./pyramid_sacrud_gallery/static/js/gallery.js', { debug: false })
        .bundle()
        .on('error', function (err) {
            gutil.log(gutil.colors.red('Failed to browserify'),
                      gutil.colors.yellow(err.message));
        })
        .pipe(source('__gallery.js'))
        .pipe(gulp.dest('./pyramid_sacrud_gallery/static/js/'));
});

gulp.task('css', function() {
    var path = glob.sync('./*/static/css/');
    gulp.src(getFiles(path))
        .pipe(filter('*.css'))
        .pipe(autoprefixer({
            browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9',
                       'Chrome >= 15', 'Safari >= 4', '> 1%'],
            cascade: false
        }))
        .pipe(minifyCSS())
        .pipe(concat('__gallery.css'))
        .pipe(gulp.dest(path + '/'));
});

gulp.task('watch', function () {
    var path = glob.sync('./*/static/*/');
    watch(getFiles(path), function (files, cb) {
        gulp.start('css', cb);
    });
});

gulp.task('default', ['watch']);
