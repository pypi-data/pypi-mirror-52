let autoprefixer  = require('gulp-autoprefixer');
let gulp          = require('gulp');
let plumber       = require('gulp-plumber');
let rename        = require('gulp-rename');
let sass          = require('gulp-sass');
let sourcemaps    = require('gulp-sourcemaps');
let uglify        = require('gulp-uglify');


/* Styleshets */
gulp.task('styles', function(done) {
    gulp.src('styles/**/*.sass')
        .pipe(plumber())
        .pipe(sourcemaps.init())
        .pipe(sass({
            outputStyle: 'compressed'}
            ))
        .pipe(autoprefixer("last 3 version", "safari 5", "ie 8", "ie 9"))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('css/'));
    done();
});


/* Individual Uglified Scripts */
gulp.task('scripts', function(done) {
    gulp.src('js/*.js')
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(rename({suffix: '.min'}))
        .pipe(sourcemaps.write("."))
        .pipe(gulp.dest('js/min/'));
    done();
});


// While developing, run 'gulp watch'
gulp.task('watch',function(done) {
    gulp.watch('styles/**/*.sass',['styles']);
    gulp.watch('js/*.js',['scripts']);
done();
});


// Run 'gulp' to build everything at once
gulp.task('default', gulp.series('styles', 'scripts'));
