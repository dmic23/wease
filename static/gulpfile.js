var gulp = require('gulp');
//Plugins
var gulpif = require('gulp-if');
var rename = require('gulp-rename');
var gutil = require('gulp-util');
var compass = require('gulp-compass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var ngAnnotate = require('gulp-ng-annotate')
var imagemin = require('gulp-imagemin');
var pngquant = require('imagemin-pngquant');
var connect = require('gulp-connect');
var mainBowerFiles = require('main-bower-files');
var gulpFilter = require('gulp-filter');
var inject = require('gulp-inject');
var flatten = require('gulp-flatten');
var minifycss = require('gulp-minify-css');
var minifyHTML = require('gulp-minify-html');

var env,
	jsSources,
	sassSources,
	bowerFiles,
	outputDir;

jsSources = [
	'build/development/scripts/app.js',
	'build/development/scripts/**/**.module.js',
	'build/development/scripts/authentication/**/*.js',
	'build/development/scripts/accounts/**/*.js',
	'build/development/scripts/orders/**/*.js',	
	'build/development/scripts/layout/**/*.js',
  'build/development/scripts/messages/**/*.js',
	'build/development/scripts/controllers/**/*.js',
	'build/development/scripts/directives/**/*.js',
	'build/development/scripts/modules/**/*.js',
  'build/development/scripts/filters/**/*.js',

];
sassSources = [
	'sass/main.scss'
];
cssSources = [
  'styles/wease.css'
]
bowerFiles = [
	'build/development/bower_components/jquery.min.js',
	'build/development/bower_components/angular.min.js',
	'build/development/bower_components/json3.min.js',
	'build/development/bower_components/underscore.min.js',
	'build/development/bower_components/bootstrap.min.js',
	'build/development/bower_components/*.js'
];

env = process.env.NODE_ENV || 'development';

if (env==='development') {
	outputDir = 'build/development/';
	sassStyle = 'compressed';
} else {
	outputDir = 'build/production/';
	sassStyle = 'compressed';
}

// JS concat and minify and add.min 
gulp.task('scripts', function() {
	gulp.src(jsSources)
		.pipe(concat('main.min.js'))
		// .pipe(gulpif(env === 'production', rename({ suffix: '.min'})))
		.pipe(gulpif(env === 'production', ngAnnotate()))
		.pipe(gulpif(env === 'production', uglify())
		.on('error', gutil.log))
		.pipe(gulp.dest(outputDir + 'js'))
    	// .pipe(connect.reload())
});

//SASS/CSS concat and minify
gulp.task('compass', function() {
	gulp.src(sassSources)
		.pipe(compass({
			sass: 'sass',
			css: outputDir + 'css',
			image: outputDir + 'images',
			style: sassStyle,
		})
		.on('error', gutil.log))
		.pipe(gulp.dest(outputDir + 'css'))
		// .pipe(connect.reload())
});

//Image compress for production only
gulp.task('images', function() {
  gulp.src('build/development/images/*.*')
  	.pipe(gulpif(env === 'production', imagemin({
  		progressive : true,
  		svgoPlugins: [{ removeViewBox: false }],
  		use: [pngquant()]
  	})))
  	.pipe(gulpif(env === 'production', gulp.dest(outputDir+'images')))
  	// .pipe(connect.reload())
});

// grab libraries files from bower_components, minify and push in /public
gulp.task('bower', function() {
 
    var jsFilter = gulpFilter(['*.js', '!*.min.*']);
    var cssFilter = gulpFilter(['*.css', '!*.min.*']);
    var fontFilter = gulpFilter(['*.eot', '*.woff', '*.svg', '*.ttf']);
 
        return gulp.src(mainBowerFiles())
 
        // grab vendor js files from bower_components, minify and push in /public
        .pipe(jsFilter)
        .pipe(ngAnnotate())
        .pipe(uglify())
        .pipe(rename({
        suffix: ".min"
    	}))
        .pipe(gulp.dest('build/development/bower_components/')
    	.on('error', gutil.log))
        .pipe(jsFilter.restore())
 
        // grab vendor css files from bower_components, minify and push in /public
        .pipe(cssFilter)
        .pipe(gulpif(env === 'development', gulp.dest(outputDir + 'css'))
    	.on('error', gutil.log))
        .pipe(minifycss())
        .pipe(concat('bower.css'))
        .pipe(rename({
        suffix: ".min"
    	}))
        .pipe(gulp.dest(outputDir + 'css')
    	.on('error', gutil.log))
        .pipe(cssFilter.restore())
 
        // grab vendor font files from bower_components and push in /public
        .pipe(fontFilter)
        .pipe(flatten())
        .pipe(gulp.dest(outputDir + 'fonts')
    	.on('error', gutil.log))
});

// Bower concat and minify and add.min 
gulp.task('bowerConcat', ['bower'], function() {
	gulp.src(bowerFiles)
        .pipe(ngAnnotate())
		.pipe(concat('bower.min.js'))
		.pipe(gulp.dest(outputDir + 'js'))
});

// gulp.task('html', function() {
// 	gulp.src('build/development/*.html')
// 		.pipe(gulpif(env === 'production', minifyHTML()))
// 		.pipe(gulpif(env === 'production', gulp.dest(outputDir)))
// 		// .pipe(connect.reload())
// });

gulp.task('views', function() {
	gulp.src('build/development/views/**/*.*')
		.pipe(gulpif(env === 'production', gulp.dest(outputDir + 'views')))
		// .pipe(connect.reload())
});

gulp.task('vendor', function() {
	gulp.src('build/development/scripts/vendor/**/*.*')
		.pipe(gulpif(env === 'production', gulp.dest(outputDir + 'scripts/vendor')))
		// .pipe(connect.reload())
});

//Watch for changes in the js, css and image files
gulp.task('watch', function() {
  gulp.watch(jsSources, ['js']);
  gulp.watch('sass/*.scss', ['compass']);
  // gulp.watch('builds/development/*.html', ['html']);
  gulp.watch('images/*.*', ['images']);
  gulp.watch('build/development/views/**/*.*', ['views']);
  gulp.watch('build/development/scripts/vendor/**/*.*', ['vendor']);
});

// Live reload upon changes to files
gulp.task('connect', function() {
  connect.server({
    root: '../templates/',
    port: 8000,
    livereload: true
  });
});

// Build runs
gulp.task('default', ['bower', 'scripts', 'compass', 'images', 'views', 'vendor', 'bowerConcat']);
