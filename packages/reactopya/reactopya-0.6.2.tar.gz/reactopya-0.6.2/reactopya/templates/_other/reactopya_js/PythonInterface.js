import PythonProcess from './PythonProcess';
const stable_stringify = require('json-stable-stringify');

export default class PythonInterface {
    constructor(reactComponent, config) {
        this._reactComponent = reactComponent;
        this._pythonModuleName = config.pythonModuleName || '{{ project_name }}_widgets';
        this._type = config.type;
        this._syncPythonStateToStateKeys = config.pythonStateKeys;
        this._syncStateToJavaScriptStateKeys = config.javaScriptStateKeys;
        this._pythonProcess = null;
        this._pythonState = {};
        this._javaScriptState = {};
        this._pendingJavaScriptState = {};
    }
    start() {
        console.info(`Starting python interface for ${this._reactComponent.constructor.name}`);
        if (this._reactComponent.props.reactopya_init_state) {
            // this is for snapshots (static html exports)
            this._reactComponent.setState(this._reactComponent.props.reactopya_init_state);
        }
        if (this._reactComponent.props.javaScriptPythonStateModel) {
            this._reactComponent.props.javaScriptPythonStateModel.onPythonStateChanged((state) => {
                this._reactComponent.setState(state);
            });
        }
        else {
            if ((!window.reactopya) || (!window.reactopya.disable_python_backend)) {
                if (!this._pythonProcess) {
                    this._pythonProcess = new PythonProcess(this._pythonModuleName, this._type);
                    this._pythonProcess.onReceiveMessage(this._handleReceiveMessageFromProcess);
                    this._pythonProcess.start();
                }
            }
            else {
                console.info('Python backend disabled');
            }
            window.addEventListener('beforeunload', () => {
                this.stop();
                window.removeEventListener('beforeunload', this._cleanup); // remove the event handler for normal unmounting
            });
            if (Object.keys(this._pendingJavaScriptState).length > 0) {
                this.setJavaScriptState(this._pendingJavaScriptState);
                this._pendingJavaScriptState = {};
            }
        }
        this.update();
    }
    stop() {
        this._cleanup();
    }
    update() {
        this._copyStateToJavaScriptState();
    }
    setJavaScriptState(state) {
        if ((!this._reactComponent.props.javaScriptPythonStateModel) && (!this._pythonProcess)) {
            for (let key in state) {
                this._pendingJavaScriptState[key] = state[key];
            }
            return;
        }
        let newJavaScriptState = {};
        for (let key in state) {
            if (!compare(state[key], this._javaScriptState[key])) {
                this._javaScriptState[key] = clone(state[key]);
                newJavaScriptState[key] = clone(state[key]);
            }
        }
        if (Object.keys(newJavaScriptState).length > 0) {
            if (this._reactComponent.props.javaScriptPythonStateModel) {
                this._reactComponent.props.javaScriptPythonStateModel.setJavaScriptState(newJavaScriptState);
            }
            else if (this._pythonProcess) {
                this._pythonProcess.sendMessage({
                    name: 'setJavaScriptState',
                    state: newJavaScriptState
                });
            }
            else {
                console.error('Problem in setJavaScriptState: unable to find one of: props.javaScriptPythonStateModel, _pythonProcess');
            }
        }
    }
    getJavaScriptState(key) {
        if (key in this._javaScriptState) {
            return JSON.parse(JSON.stringify(this._javaScriptState[key]));
        }
        else return undefined;
    }

    getPythonState(key) {
        if (key in this._pythonState) {
            return JSON.parse(JSON.stringify(this._pythonState[key]));
        }
        else return undefined;
    }

    _cleanup() {
        if (!this._reactComponent.props.javaScriptPythonStateModel) {
            if (this._pythonProcess) {
                this._pythonProcess.stop();
                this._pythonProcess = null;
            }
        }
    }

    _handleReceiveMessageFromProcess = (msg) => {
        if (msg.name == 'setPythonState') {
            let somethingChanged = false;
            for (let key in msg.state) {
                if (!compare(msg.state[key], this._pythonState[key])) {
                    this._pythonState[key] = clone(msg.state[key]);
                    somethingChanged = true;
                }
            }
            if (somethingChanged) {
                this._copyPythonStateToState(this._syncPythonStateToStateKeys);
            }
        }
    }

    _copyPythonStateToState(keys) {
        let newState = {};
        for (let key of keys) {
            if (!compare(this._pythonState[key], this._reactComponent.state[key])) {
                newState[key] = clone(this._pythonState[key]);
            }
        }
        this._reactComponent.setState(newState);
    }
    _copyStateToJavaScriptState() {
        let newState = {};
        for (let key of this._syncStateToJavaScriptStateKeys) {
            if (!compare(this.getJavaScriptState[key], this._reactComponent.state[key])) {
                newState[key] = clone(this._reactComponent.state[key]);
            }
        }
        if (Object.keys(newState).length > 0) {
            this.setJavaScriptState(newState);
        }
    }
}

function compare(a, b) {
    if ((a === undefined) && (b === undefined))
        return true;
    if ((a === null) && (b === null))
        return true;
    return (stable_stringify(a) === stable_stringify(b));
}

function clone(a) {
    if (a === undefined)
        return undefined;
    if (a === null)
        return null;
    return JSON.parse(stable_stringify(a));
}

function _json_parse(x) {
    try {
        return JSON.parse(x);
    }
    catch(err) {
        return null;
    }
}

function _json_stringify(x) {
    try {
        return JSON.stringify(x);
    }
    catch(err) {
        return '';
    }
}

