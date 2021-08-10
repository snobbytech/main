import * as firebase from "firebase"
import { firestore } from "./base";

/*
    This file is a series of util functions for interacting with
    current-user profiles.

    TODO:
      - Firebase has some thresholds for free usage, so if we start
        doing too many read/writes we'll have to think about batching or
        switching to another service.
*/


// I'm sorry, this promise chaining is so stupid. I'm going to make this async
// and call an await in here.
export const getSearchProfile = async (uid) => {
    // If there's nothing.. then we return nothing.
    var cur_user = firestore.collection('users').doc(uid);
    var ret_dict = {'clients': [], 'keywords': [], 'searches': [], 'linkedin_url': ''}

    var user_doc = await cur_user.get();
    if (user_doc.exists) {
        let the_data = user_doc.data();
        if ('clients' in the_data) {
            ret_dict.clients = the_data.clients.join('\n');
        }
        if ('keywords' in the_data) {
            ret_dict.keywords = the_data.keywords.join('\n');
        }
        if ('searches' in the_data) {
            ret_dict.searches = the_data.searches;
        }
        if ('linkedin_url' in the_data) {
            ret_dict.linkedin_url = the_data.linkedin_url
        }

    }
    return ret_dict;
}


// Update the user profile.
export const setSearchProfile = (uid, searchProfileDict) => {
    var cur_user = firestore.collection('users').doc(uid);

    // Update the data?
    cur_user.set(searchProfileDict, {merge: true}).then(()=> {
        return true;
    })
    // We're not so happy in this case.
    return false;
}

// If a user searched a prospect, make a note of it.
// Values searchee_id, searchee_linkedin, searchee_name, searchee_company_name
export const userSearchedProfile = async (uid, search_dict) => {
    var cur_user = firestore.collection('users').doc(uid);
    let searches = [];
    cur_user.get().then((doc) => {
        if (doc.exists) {
            // Then we can update it.
            if ('searches' in doc.data()) {
                searches = doc.data().searches;
            }

            let should_append = true;
            for (let i=0; i < searches.length; i++) {
                // Don't add repeats.
                if (searches[i].linkedin_url == search_dict.linkedin_url) {
                    should_append = false;
                }
            }
            if (should_append) {
                searches.unshift(search_dict);
            }
            // Write the doc.
            cur_user.set({'searches': searches}, {merge: true});
            // No "then".  Let's just let sleepy dogs be sleepy.
        }
    })
}


// TODO: make this happen. I think this is more important when
//       we're doing batch processing.
export const getSearchedPeople = (uid) => {
    // Return a list of names and quick-access links

}


