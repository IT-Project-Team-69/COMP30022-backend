import React from "react";
import InputField from "../components/InputField";
import AuthController from "../controllers/AuthController";
import "./Profile.css";

/**
 * Profile Page
 * - Shows user their account information
 * - Allows user to modify their account information
 */
class Profile extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            buttonDisabled: true,
            photoURL: "",
            firstName: "",
            lastName: "",
            email: "",
            organisation: "",
            role: "",
            phone: "",
            link: "",
            emailError: "",
            emailValid: true,
        };
    }

    // TODO: CONNECT WITH PFOFILE API
    componentDidMount() {
        const profileAPI = "";
        // data = await fetch(profileAPI);
        this.setState({
            photoURL:
                "https://techcommunity.microsoft.com/t5/image/serverpage/image-id/217078i525F6A9EF292601F/image-size/large?v=v2&px=999",
            firstName: "First Name",
            lastName: "Last Name",
            email: "first.last@gmail.com",
        });
    }

    changeHandler = async (event) => {
        this.setState({
            [event.target.name]: event.target.value,
            buttonDisabled: false,
        });
    };

    emailChangeHandler = async (event) => {
        await this.setState({
            [event.target.name]: event.target.value,
        });
        let result = await AuthController.emailChangeHandler(this.state.email);
        this.setState({
            emailError: result.error,
            emailValid: result.valid,
            buttonDisabled: false,
        });
    };

    render() {
        return (
            <div className="profile-content">
                <div className="form">
                    <h3>Public Contact Details</h3>
                    <div className="profile-photo-row">
                        <img
                            className="profile-photo"
                            src={this.state.photoURL}
                        ></img>
                    </div>
                    <InputField
                        type="text"
                        name="firstName"
                        label="First Name"
                        placeholder="e.g. Jane"
                        onChange={this.changeHandler}
                        value={this.state.firstName}
                    />
                    <InputField
                        type="text"
                        name="lastName"
                        label="Last Name"
                        placeholder="e.g. Doe"
                        onChange={this.changeHandler}
                        value={this.state.lastName}
                    />
                    <InputField
                        type="email"
                        name="email"
                        label="Email Address"
                        placeholder="e.g. jane.doe@email.com"
                        onChange={this.emailChangeHandler}
                        value={this.state.email}
                    />
                    <InputField
                        type="text"
                        name="organisation"
                        label="Organisation"
                        placeholder="e.g. Hogwarts"
                        onChange={this.changeHandler}
                        value={this.state.organisation}
                    />
                    <InputField
                        type="text"
                        name="role"
                        label="Role"
                        placeholder="e.g. Wizard"
                        onChange={this.changeHandler}
                        value={this.state.role}
                    />
                    <InputField
                        type="text"
                        name="phone"
                        label="Phone Number"
                        placeholder="e.g. +61 302 203 392"
                        onChange={this.changeHandler}
                        value={this.state.phone}
                    />
                    <InputField
                        type="url"
                        name="link"
                        label="LinkedIn URL"
                        placeholder="e.g. linkedin.com/in/jane-doe"
                        onChange={this.changeHandler}
                        value={this.state.phone}
                    />
                    <div className="button-row">
                        <button className="invisible-button" />
                        <button className="primary-button" disabled={this.state.buttonDisabled}>SAVE</button>
                    </div>
                </div>
            </div>
        );
    }
}

export default Profile;
