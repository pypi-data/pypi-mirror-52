var LiveReloadPlugin = require('webpack-livereload-plugin');


module.exports = {
    mode: "development",

    entry: "./ts/index.tsx",
    output: {
        filename: "bundle.js",
        path: __dirname + "/claude/static",
        libraryTarget: 'umd',
    },

    // Enable sourcemaps for debugging webpack's output.
    devtool: "source-map",

    resolve: {
        // Add '.ts' and '.tsx' as resolvable extensions.
        extensions: [".ts", ".tsx", ".js"]
    },

    module: {
        rules: [
            {
                test: /\.ts(x?)$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: "ts-loader"
                    }
                ]
            },
            // All output '.js' files will have any sourcemaps re-processed by 'source-map-loader'.
            {
                enforce: "pre",
                test: /\.js$/,
                loader: "source-map-loader"
            }
        ]
    },

    // When importing a module whose path matches one of the following, just
    // assume a corresponding global variable exists and use that instead.
    // This is important because it allows us to avoid bundling all of our
    // dependencies, which allows browsers to cache those libraries between builds.
    externals: {
        "react": "React",
        "react-dom": "ReactDOM",
        "@material-ui/core": "MaterialUI",
        "@fortawesome/free-solid-svg-icons": "free-solid-svg-icons",
        "@fortawesome/free-brands-svg-icons": "free-brands-svg-icons",
        "@fortawesome/fontawesome-svg-core": "fontawesome-svg-core",
        "moment": "moment",
        "react-draggable": "ReactDraggable",
        "recharts": "Recharts",
        "react-redux": "ReactRedux",
        "prop-types": "PropTypes",

        // 6.43MB vs 0.29 MB

        /** MORE:
         * react-rnd
         * @fortawesome/react-fontawesome
         *
         */
    },

    plugins: [
        new LiveReloadPlugin({})
    ]
};
