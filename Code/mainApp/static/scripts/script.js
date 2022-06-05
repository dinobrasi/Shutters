/*jshint esversion: 6 */
/*jshint -W097 */
"use strict";
/* 2022-05-07 */

var api_relay_floor_first = "192.168.0.230";
var api_relay_floor_second = "192.168.0.46";

if (!window.console) {
	console = { log: function () { }, warn: function () { } };
}
var showconsoledebugmsgs = true;
var debugprefix = "[dw] ";
var showconsoledebugmsgs = true;
var welcome_banner = "  ____                                      _   __  __" + "\n" +
	" |  _ \\  ___   __ ___      _____   ___   __| | |  \\/  | __ _ _ __   ___  _ __ " + "\n" +
	" | | | |/ _ \\ / _` \\ \\ /\\ / / _ \\ / _ \\ / _` | | |\\/| |/ _` | '_ \\ / _ \\| '__|" + "\n" +
	" | |_| | (_) | (_| |\\ V  V / (_) | (_) | (_| | | |  | | (_| | | | | (_) | |   " + "\n" +
	" |____/ \\___/ \\__, | \\_/\\_/ \\___/ \\___/ \\__,_| |_|  |_|\\__,_|_| |_|\\___/|_|   " + "\n" +
	"              |___/" + "\n" +
	"Welcome. If you are having a problem with the tool, please email Tim.";

var touchcount = 0;
var activeborder = "border-applemsg";
/*
 * id = dom element
 * key = relay #
 * name = name, duh
 * direction = up or dn
 * state = on or off
 */
var clsActiveWindow = {
	id: "",
	key: -1,
	floor: 0,
	name: "",
	direction: "",
	state: "off"
};
var setActiveWindow = function (direction, id, key, name, state) {
	clsActiveWindow.direction = direction;
	clsActiveWindow.id = id;
	clsActiveWindow.key = key;
	clsActiveWindow.name = name;
	clsActiveWindow.state = state;
};
var clearActiveWindow = function () {
	clsActiveWindow.id = "";
	clsActiveWindow.key = -1;
	clsActiveWindow.floor = 0;
	clsActiveWindow.name = "";
	clsActiveWindow.direction = "";
	clsActiveWindow.state = "off";
};
var doDebugMsg = function (strMsg) {
	doDebugMsg(strMsg, "black");
};
var doDebugMsg = function (strMsg, color) {
	if (showconsoledebugmsgs) {
		if (color === "") {
			console.log(strMsg);
		}
		else {
			console.log("%c" + strMsg, "color:" + color);
		}
	}
};
function handleStart(event) {
	if (event.cancelable) event.preventDefault();
	doDebugMsg(`${debugprefix}Touch - Start`, "RED");
	$("#spinner").removeClass("d-none");
	$(".windr").removeClass(activeborder);
	var id = event.target.id;
	$(`#${id}`).addClass(activeborder);
	const myArray = id.split("-");
	var name = myArray[0];
	var direction = myArray[1];
	var key = getWindowIdFromName(name);
	var state = "on";
	processStart(direction, id, key, name, state);
}
var processStart = function (direction, id, key, name, state) {
	doDebugMsg(`${debugprefix}${id}, ${name}, ${direction}, ${key} - ON`, "GREEN");
	setActiveWindow(direction, id, key, name, state);
	sendCommand(clsActiveWindow);
};
function handleMove(event) {
	if (event.cancelable) event.preventDefault();
	touchcount += 1;
	if (clsActiveWindow.id !== "") {
		if (touchcount >= 10) {
			doDebugMsg(`${debugprefix}Touch - End (because of move)`, "RED");
			processEnd("off");
		}
	}
}
function handleEnd(event) {
	if (event.cancelable) event.preventDefault();
	doDebugMsg(`${debugprefix}Touch - End`, "RED");
	$("#spinner").addClass("d-none");
	var state = "off";
	processEnd(state);
}
var processEnd = function (state) {
	if (clsActiveWindow.id !== "") {
		doDebugMsg(`${debugprefix}${clsActiveWindow.id}, ${clsActiveWindow.name}, ${clsActiveWindow.direction}, ${clsActiveWindow.key} - OFF`, "GREEN");
		clsActiveWindow.state = state;
		sendCommand(clsActiveWindow);
		clearActiveWindow();
	}
	$(".windr").removeClass(activeborder);
	touchcount = 0;
};
function handleCancel(event) {
	doDebugMsg(`${debugprefix}handleCancel`, "PURPLE");
	if (event.cancelable) event.preventDefault();
	doDebugMsg(`${debugprefix}touchcancel`);
}
var getWindowIdFromName = function (name) {
	var returnValue = 0;
	switch (name) {
		case "office_west_south": returnValue = 1; break;
		case "garage_north": returnValue = 2; break;
		case "sitting_south_east": returnValue = 3; break;
		case "office_south_east": returnValue = 4; break;
		case "livingroom_north_west": returnValue = 5; break;
		case "kitchen_east": returnValue = 6; break;
		case "livingroom_west_south": returnValue = 7; break;
		case "kitchen_north_west": returnValue = 8; break;
		case "office_west_north": returnValue = 9; break;
		case "garage_south": returnValue = 10; break;
		case "sitting_south_west": returnValue = 11; break;
		case "office_south_west": returnValue = 12; break;
		case "kitchen_north_east": returnValue = 13; break;
		case "sitting_east": returnValue = 14; break;
		case "livingroom_west_north": returnValue = 15; break;
		case "livingroom_north_east": returnValue = 16; break;
		case "rotunda_skylight_2": returnValue = 17; break;
		case "library_west_north": returnValue = 18; break;
		case "castle_south_west": returnValue = 19; break;
		case "library_south_west": returnValue = 20; break;
		case "master_north_east": returnValue = 21; break;
		case "castle_east": returnValue = 22; break;
		case "guest_west_north": returnValue = 23; break;
		case "guest_north_east": returnValue = 24; break;
		case "rotunda_skylight_1": returnValue = 25; break;
		case "library_west_south": returnValue = 26; break;
		case "castle_south_east": returnValue = 27; break;
		case "library_south_east": returnValue = 28; break;
		case "master_north_west": returnValue = 29; break;
		case "guest_west_south": returnValue = 30; break;
		case "master_east": returnValue = 31; break;
		case "guest_north_west": returnValue = 32; break;
		default: break;
	}
	return returnValue;
};
var sendCommand = function (objWindow) {
	var hostname;
	if (objWindow.key <= 16) {
		hostname = api_relay_floor_first;
	}
	else {
		hostname = api_relay_floor_second;
	}
	var url = `http://${hostname}:4449/window/${objWindow.key}/${objWindow.direction}/${objWindow.state}`;
	doDebugMsg(`${debugprefix}Sending Command(${url}`);
	$.ajax({
		type: "get",
		url: url,
		dataType: "json"
	})
		.done(function (request) {
			doDebugMsg(`${debugprefix}Command Success!`);
		})
		.fail(function (error) {
			doDebugMsg(`${debugprefix}Command Error!`);
		});
};

$(function () {
	console.log(welcome_banner);
	doDebugMsg(`${debugprefix}Page Load: Start`);

	$(".windr").on("touchstart", handleStart);
	$(".windr").on("touchend", handleEnd);
	$(".windr").on("touchmove", handleMove);
	$(".windr").on("touchcancel", handleCancel);
	$(".windr").on("mousedown", handleStart);
	$(".windr").on("mouseup", handleEnd);

	doDebugMsg(`${debugprefix}Page Load: Complete`);
});