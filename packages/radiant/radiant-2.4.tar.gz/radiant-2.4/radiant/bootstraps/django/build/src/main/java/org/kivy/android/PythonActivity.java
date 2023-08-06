//radiant

package org.kivy.android;

import java.net.Socket;
import java.net.InetSocketAddress;

import android.os.SystemClock;

import java.io.InputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.File;
import java.io.IOException;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.ArrayList;

import android.app.*;
import android.content.*;
import android.view.*;
import android.view.ViewGroup;
import android.view.SurfaceView;
import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.widget.Toast;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.PowerManager;
import android.graphics.PixelFormat;
import android.view.SurfaceHolder;
import android.content.Context;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.content.pm.ApplicationInfo;
import android.content.Intent;
import android.widget.ImageView;
import java.io.InputStream;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;

import android.widget.AbsoluteLayout;
import android.view.ViewGroup.LayoutParams;

import android.webkit.WebViewClient;
import android.webkit.WebView;

import org.kivy.android.PythonUtil;

import org.kivy.android.WebViewLoader;

import org.renpy.android.ResourceManager;
import org.renpy.android.AssetExtract;

//radiant
//----------------------------------------------------------
import android.view.WindowManager;
import android.view.Window;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.PermissionRequest;
import android.webkit.JavascriptInterface;
import android.webkit.WebBackForwardList;
import android.webkit.WebSettings;
import android.webkit.DownloadListener;
import android.app.DownloadManager;
import android.os.Environment;
import android.net.Uri;
import android.app.DownloadManager.Request;
import android.os.Build;
import android.os.StrictMode;
import java.lang.reflect.InvocationTargetException;
//import java.lang.StringBuilder;
//----------------------------------------------------------



public class PythonActivity extends Activity {
    // This activity is modified from a mixture of the SDLActivity and
    // PythonActivity in the SDL2 bootstrap, but removing all the SDL2
    // specifics.

    private static final String TAG = "PythonActivity";

    public static PythonActivity mActivity = null;

    /** If shared libraries (e.g. SDL or the native application) could not be loaded. */
    public static boolean mBrokenLibraries;

    protected static ViewGroup mLayout;
    protected static WebView mWebView;

    protected static Thread mPythonThread;

    private ResourceManager resourceManager = null;
    private Bundle mMetaData = null;
    private PowerManager.WakeLock mWakeLock = null;

    public String getAppRoot() {
        String app_root =  getFilesDir().getAbsolutePath() + "/app";
        return app_root;
    }

    public String getEntryPoint(String search_dir) {
        /* Get the main file (.pyc|.pyo|.py) depending on if we
         * have a compiled version or not.
        */
        List<String> entryPoints = new ArrayList<String>();
        entryPoints.add("main.pyo");  // python 2 compiled files
        entryPoints.add("main.pyc");  // python 3 compiled files
                for (String value : entryPoints) {
            File mainFile = new File(search_dir + "/" + value);
            if (mainFile.exists()) {
                return value;
            }
        }
        return "main.py";
    }
    
    //radiant
    //----------------------------------------------------------
    public void setThemeColor(String status_bar_color, String navigation_bar_color, String mode) {
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Window window = mActivity.getWindow();
            window.clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS);
            window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
            window.setStatusBarColor(Color.parseColor(status_bar_color));
            window.setNavigationBarColor(Color.parseColor(navigation_bar_color));
            //window.setStatusBarColor(Color.parseColor("{{STATUS_BAR_COLOR}}"));
            //window.setNavigationBarColor(Color.parseColor("{{NAVIGATION_BAR_COLOR}}"));
        }
        
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            View decor = mActivity.getWindow().getDecorView();
            
            if (mode.equals("light")) {
                decor.setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR |
                                            View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
                                            );
            } else {
                decor.setSystemUiVisibility(0);
            }
            
        }
        
    }
    //----------------------------------------------------------

    public static void initialize() {
        // The static nature of the singleton and Android quirkyness force us to initialize everything here
        // Otherwise, when exiting the app and returning to it, these variables *keep* their pre exit values
        mWebView = null;
        mLayout = null;
        mBrokenLibraries = false;
    
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Log.v(TAG, "My oncreate running");
        resourceManager = new ResourceManager(this);

        Log.v(TAG, "Ready to unpack");
        File app_root_file = new File(getAppRoot());
        unpackData("private", app_root_file);

        Log.v(TAG, "About to do super onCreate");
        super.onCreate(savedInstanceState);
        Log.v(TAG, "Did super onCreate");

        this.mActivity = this;
        //this.showLoadingScreen();
        Log.v("Python", "Device: " + android.os.Build.DEVICE);
        Log.v("Python", "Model: " + android.os.Build.MODEL);

        //Log.v(TAG, "Ready to unpack");
        //new UnpackFilesTask().execute(getAppRoot());

        PythonActivity.initialize();

        // Load shared libraries
        String errorMsgBrokenLib = "";
        try {
            loadLibraries();
        } catch(UnsatisfiedLinkError e) {
            System.err.println(e.getMessage());
            mBrokenLibraries = true;
            errorMsgBrokenLib = e.getMessage();
        } catch(Exception e) {
            System.err.println(e.getMessage());
            mBrokenLibraries = true;
            errorMsgBrokenLib = e.getMessage();
        }

        if (mBrokenLibraries)
        {
            AlertDialog.Builder dlgAlert  = new AlertDialog.Builder(this);
            dlgAlert.setMessage("An error occurred while trying to load the application libraries. Please try again and/or reinstall."
                  + System.getProperty("line.separator")
                  + System.getProperty("line.separator")
                  + "Error: " + errorMsgBrokenLib);
            dlgAlert.setTitle("Python Error");
            dlgAlert.setPositiveButton("Exit",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog,int id) {
                        // if this button is clicked, close current activity
                        PythonActivity.mActivity.finish();
                    }
                });
           dlgAlert.setCancelable(false);
           dlgAlert.create().show();

           return;
        }
        
        

        // Set up the webview
        String app_root_dir = getAppRoot();

        mWebView = new WebView(this);
        mWebView.getSettings().setJavaScriptEnabled(true);
        mWebView.getSettings().setDomStorageEnabled(true);

        //django-for-android
        //----------------------------------------------------------
        mWebView.setVerticalScrollBarEnabled(false);
        mWebView.getSettings().setAllowFileAccess(true);
         if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN) {
            mWebView.getSettings().setAllowFileAccessFromFileURLs(true);
            mWebView.getSettings().setAllowUniversalAccessFromFileURLs(true);
         }

        mWebView.getSettings().setCacheMode(WebSettings.LOAD_NO_CACHE);
        class MyJavaScriptInterface {
           @JavascriptInterface
           public String toString() { return "injectedObject"; }
        }
        mWebView.addJavascriptInterface(new MyJavaScriptInterface(), "injectedObject");
        Log.v("D4A", "Loading splash");
        //mWebView.loadUrl("file:///" + mActivity.getFilesDir().getAbsolutePath() + "/resources/splash.html");
        mWebView.loadUrl("file:///" + app_root_dir + "/resources/splash.html");
        //----------------------------------------------------------
        //mWebView.loadUrl("file:///" + app_root_dir + "/_load.html");

        mWebView.setLayoutParams(new LayoutParams(LayoutParams.FILL_PARENT, LayoutParams.FILL_PARENT));
        mWebView.setWebViewClient(new WebViewClient() {
                //@Override
                public boolean shouldOverrideUrlLoading(WebView view, String url) {
                    view.loadUrl(url);
                    return false;
                }
            });
            
            
        //radiant
        //----------------------------------------------------------
        mWebView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                Log.d(TAG, "onPermissionRequest");
                runOnUiThread(new Runnable() {
                    //@TargetApi(Build.VERSION_CODES.LOLLIPOP)
                    @Override
                    public void run() {
                      request.grant(request.getResources());
                    }
                });
            }
        });
        //----------------------------------------------------------

        mLayout = new AbsoluteLayout(this);
        mLayout.addView(mWebView);

        setContentView(mLayout);

        String mFilesDirectory = mActivity.getFilesDir().getAbsolutePath();
        String entry_point = getEntryPoint(app_root_dir);

        Log.v(TAG, "Setting env vars for start.c and Python to use");
        PythonActivity.nativeSetenv("ANDROID_ENTRYPOINT", entry_point);
        PythonActivity.nativeSetenv("ANDROID_ARGUMENT", app_root_dir);
        PythonActivity.nativeSetenv("ANDROID_APP_PATH", app_root_dir);
        PythonActivity.nativeSetenv("ANDROID_PRIVATE", mFilesDirectory);
        PythonActivity.nativeSetenv("ANDROID_UNPACK", app_root_dir);
        PythonActivity.nativeSetenv("PYTHONHOME", app_root_dir);
        PythonActivity.nativeSetenv("PYTHONPATH", app_root_dir + ":" + app_root_dir + "/lib");
        PythonActivity.nativeSetenv("PYTHONOPTIMIZE", "2");

        try {
            Log.v(TAG, "Access to our meta-data...");
            mActivity.mMetaData = mActivity.getPackageManager().getApplicationInfo(
                    mActivity.getPackageName(), PackageManager.GET_META_DATA).metaData;

            PowerManager pm = (PowerManager) mActivity.getSystemService(Context.POWER_SERVICE);
            if ( mActivity.mMetaData.getInt("wakelock") == 1 ) {
                mActivity.mWakeLock = pm.newWakeLock(PowerManager.SCREEN_BRIGHT_WAKE_LOCK, "Screen On");
                mActivity.mWakeLock.acquire();
            }
        } catch (PackageManager.NameNotFoundException e) {
        }

        final Thread pythonThread = new Thread(new PythonMain(), "PythonThread");
        PythonActivity.mPythonThread = pythonThread;
        pythonThread.start();

        final Thread wvThread = new Thread(new WebViewLoaderMain(), "WvThread");
        wvThread.start();

    }

    @Override
    public void onDestroy() {
        Log.i("Destroy", "end of app");
        super.onDestroy();

        // make sure all child threads (python_thread) are stopped
        android.os.Process.killProcess(android.os.Process.myPid());
    }

    public void loadLibraries() {
        String app_root = new String(getAppRoot());
        File app_root_file = new File(app_root);
        PythonUtil.loadLibraries(app_root_file,
            new File(getApplicationInfo().nativeLibraryDir));
    }

    public void recursiveDelete(File f) {
        if (f.isDirectory()) {
            for (File r : f.listFiles()) {
                recursiveDelete(r);
            }
        }
        f.delete();
    }

    /**
     * Show an error using a toast. (Only makes sense from non-UI
     * threads.)
     */
    public void toastError(final String msg) {

        final Activity thisActivity = this;

        runOnUiThread(new Runnable () {
            public void run() {
                Toast.makeText(thisActivity, msg, Toast.LENGTH_LONG).show();
            }
        });

        // Wait to show the error.
        synchronized (this) {
            try {
                this.wait(1000);
            } catch (InterruptedException e) {
            }
        }
    }

    public void unpackData(final String resource, File target) {

        Log.v(TAG, "UNPACKING!!! " + resource + " " + target.getName());

        // The version of data in memory and on disk.
        String data_version = resourceManager.getString(resource + "_version");
        String disk_version = null;

        Log.v(TAG, "Data version is " + data_version);

        // If no version, no unpacking is necessary.
        if (data_version == null) {
            return;
        }

        // Check the current disk version, if any.
        String filesDir = target.getAbsolutePath();
        String disk_version_fn = filesDir + "/" + resource + ".version";

        try {
            byte buf[] = new byte[64];
            InputStream is = new FileInputStream(disk_version_fn);
            int len = is.read(buf);
            disk_version = new String(buf, 0, len);
            is.close();
        } catch (Exception e) {
            disk_version = "";
        }

        // If the disk data is out of date, extract it and write the
        // version file.
        // if (! data_version.equals(disk_version)) {
        if (! data_version.equals(disk_version)) {
            Log.v(TAG, "Extracting " + resource + " assets.");

            recursiveDelete(target);
            target.mkdirs();

            AssetExtract ae = new AssetExtract(this);
            if (!ae.extractTar(resource + ".mp3", target.getAbsolutePath())) {
                toastError("Could not extract " + resource + " data.");
            }

            try {
                // Write .nomedia.
                new File(target, ".nomedia").createNewFile();

                // Write version file.
                FileOutputStream os = new FileOutputStream(disk_version_fn);
                os.write(data_version.getBytes());
                os.close();
            } catch (Exception e) {
                Log.w("python", e);
            }
        }
    }

    public static void loadUrl(String url) {
        class LoadUrl implements Runnable {
            private String mUrl;

            public LoadUrl(String url) {
                mUrl = url;
            }

            public void run() {
                mWebView.loadUrl(mUrl);
            }
        }

        Log.i(TAG, "Opening URL: " + url);
        mActivity.runOnUiThread(new LoadUrl(url));
    }

    public static ViewGroup getLayout() {
        return   mLayout;
    }

    long lastBackClick = SystemClock.elapsedRealtime();
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        // Check if the key event was the Back button and if there's history
        //if ((keyCode == KeyEvent.KEYCODE_BACK) && mWebView.canGoBack()) {
            //mWebView.goBack();
            //return true;
        //}
        
        //radiant
        //----------------------------------------------------------
        //Back stop in splash
        if ((keyCode == KeyEvent.KEYCODE_BACK) && mWebView.canGoBack()) {
            WebBackForwardList mWebBackForwardList = mWebView.copyBackForwardList();
            String previous = mWebBackForwardList.getItemAtIndex(mWebBackForwardList.getCurrentIndex() - 1).getUrl();
            if (! previous.endsWith("splash.html")) {
                mWebView.goBack();
                return true;
            }
        }
        //----------------------------------------------------------
        
        // If it wasn't the Back key or there's no web page history, bubble up to the default
        // system behavior (probably exit the activity)
        if (SystemClock.elapsedRealtime() - lastBackClick > 2000){
            lastBackClick = SystemClock.elapsedRealtime();
            Toast.makeText(this, "Click again to close the app",
            Toast.LENGTH_LONG).show();
            return true;
        }

        lastBackClick = SystemClock.elapsedRealtime();
        return super.onKeyDown(keyCode, event);
    }


    //----------------------------------------------------------------------------
    // Listener interface for onNewIntent
    //

    public interface NewIntentListener {
        void onNewIntent(Intent intent);
    }

    private List<NewIntentListener> newIntentListeners = null;

    public void registerNewIntentListener(NewIntentListener listener) {
        if ( this.newIntentListeners == null )
            this.newIntentListeners = Collections.synchronizedList(new ArrayList<NewIntentListener>());
        this.newIntentListeners.add(listener);
    }

    public void unregisterNewIntentListener(NewIntentListener listener) {
        if ( this.newIntentListeners == null )
            return;
        this.newIntentListeners.remove(listener);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        if ( this.newIntentListeners == null )
            return;
        this.onResume();
        synchronized ( this.newIntentListeners ) {
            Iterator<NewIntentListener> iterator = this.newIntentListeners.iterator();
            while ( iterator.hasNext() ) {
                (iterator.next()).onNewIntent(intent);
            }
        }
    }

    //----------------------------------------------------------------------------
    // Listener interface for onActivityResult
    //

    public interface ActivityResultListener {
        void onActivityResult(int requestCode, int resultCode, Intent data);
    }

    private List<ActivityResultListener> activityResultListeners = null;

    public void registerActivityResultListener(ActivityResultListener listener) {
        if ( this.activityResultListeners == null )
            this.activityResultListeners = Collections.synchronizedList(new ArrayList<ActivityResultListener>());
        this.activityResultListeners.add(listener);
    }

    public void unregisterActivityResultListener(ActivityResultListener listener) {
        if ( this.activityResultListeners == null )
            return;
        this.activityResultListeners.remove(listener);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
        if ( this.activityResultListeners == null )
            return;
        this.onResume();
        synchronized ( this.activityResultListeners ) {
            Iterator<ActivityResultListener> iterator = this.activityResultListeners.iterator();
            while ( iterator.hasNext() )
                (iterator.next()).onActivityResult(requestCode, resultCode, intent);
        }
    }

    public static void start_service(String serviceTitle, String serviceDescription,
                String pythonServiceArgument) {
        Intent serviceIntent = new Intent(PythonActivity.mActivity, PythonService.class);
        String argument = PythonActivity.mActivity.getFilesDir().getAbsolutePath();
        String filesDirectory = argument;
        String app_root_dir = PythonActivity.mActivity.getAppRoot();
        String entry_point = PythonActivity.mActivity.getEntryPoint(app_root_dir + "/service");
        serviceIntent.putExtra("androidPrivate", argument);
        serviceIntent.putExtra("androidArgument", app_root_dir);
        serviceIntent.putExtra("serviceEntrypoint", "service/" + entry_point);
        serviceIntent.putExtra("pythonName", "python");
        serviceIntent.putExtra("pythonHome", app_root_dir);
        serviceIntent.putExtra("pythonPath", app_root_dir + ":" + app_root_dir + "/lib");
        serviceIntent.putExtra("serviceTitle", serviceTitle);
        serviceIntent.putExtra("serviceDescription", serviceDescription);
        serviceIntent.putExtra("pythonServiceArgument", pythonServiceArgument);
        PythonActivity.mActivity.startService(serviceIntent);
    }

    public static void stop_service() {
        Intent serviceIntent = new Intent(PythonActivity.mActivity, PythonService.class);
        PythonActivity.mActivity.stopService(serviceIntent);
    }


    public static native void nativeSetenv(String name, String value);
    public static native int nativeInit(Object arguments);
    
    
    


    //radiant
    //----------------------------------------------------------

    /**
     * Used by android.permissions p4a module to check a permission
     **/
    public boolean checkCurrentPermission(String permission) {
        if (android.os.Build.VERSION.SDK_INT < 23)
            return true;

        try {
            java.lang.reflect.Method methodCheckPermission =
                Activity.class.getMethod("checkSelfPermission", java.lang.String.class);  
            Object resultObj = methodCheckPermission.invoke(this, permission);
            int result = Integer.parseInt(resultObj.toString());   
            if (result == PackageManager.PERMISSION_GRANTED) 
                return true;
        } catch (IllegalAccessException | NoSuchMethodException |
                 InvocationTargetException e) {
        }
        return false;
    }

    /**
     * Used by android.permissions p4a module to request runtime permissions
     **/
    public void requestPermissions(String[] permissions) {
        if (android.os.Build.VERSION.SDK_INT < 23)
            return;
        try {
            java.lang.reflect.Method methodRequestPermission =
                Activity.class.getMethod("requestPermissions",
                java.lang.String[].class, int.class);  
            methodRequestPermission.invoke(this, permissions, 1);
        } catch (IllegalAccessException | NoSuchMethodException |
                 InvocationTargetException e) {
        }
    }
    
    //----------------------------------------------------------



}


class PythonMain implements Runnable {
    @Override
    public void run() {
        PythonActivity.nativeInit(new String[0]);
    }
}

class WebViewLoaderMain implements Runnable {
    @Override
    public void run() {
        WebViewLoader.testConnection();
    }
}



