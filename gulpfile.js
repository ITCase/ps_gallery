var gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    minifyCSS = require('gulp-minify-css'),
    watch = require('gulp-watch');

var staticPath = './pyramid_sacrud_gallery/static/';
var cssFiles = [staticPath + 'css/*.css', staticPath + 'css/**/*.css', '!' + staticPath + 'css/__gallery.css'];

gulp.task('css', function() {
    gulp.src(cssFiles)
        .pipe(autoprefixer({
            browsers: [
                'Firefox >= 3',
                'Explorer >= 6',
                'Opera >= 9',
                'Chrome >= 15',
                'Safari >= 4',
                '> 1%'],
            cascade: false
        }))
        .pipe(minifyCSS())
        .pipe(concat('__gallery.css'))
        .pipe(gulp.dest(staticPath + 'css/'));
});

gulp.task('watch', function () {
    watch(cssFiles, function (files) {
        cb();
        gulp.start('css');
    });
});

gulp.task('default', function () {
    watch(cssFiles, function (files, cb) {
        cb();
        gulp.start('css');
    });
});